import hashlib

from google.cloud import datastore

client = datastore.Client()

kind = 'feedSubscriptions'


def _get_all_subscription_in_room(space):
    query = client.query(kind=kind)
    query.add_filter('space', '=', space)
    return query.fetch()


def _standardize_feed_uri(feed_uri):
    # TODO: add standardization to protocol, query & parameters
    feed_uri = feed_uri.rstrip("/")
    return feed_uri


def create(space, feed, name, creator, timestamp):
    standardized_feed = _standardize_feed_uri(feed)
    key_name = hashlib.sha1(space.encode('utf-8')+standardized_feed.encode('utf-8')).hexdigest()
    subscription_key = client.key(kind, key_name)
    subscription = datastore.Entity(key=subscription_key)
    subscription['space'] = space
    subscription['feed'] = standardized_feed
    subscription['name'] = name
    subscription['creator'] = creator
    subscription['timestamp'] = timestamp
    client.put(subscription)


def list_all(space):
    subscriptions = list(_get_all_subscription_in_room(space))
    return subscriptions


def delete_all(space):
    next_subscription = _get_all_subscription_in_room(space)
    while next_subscription:
        client.delete(next_subscription.key)


def remove_by_name(space, name):
    query = client.query(kind=kind)
    query.add_filter('space', '=', space)
    query.add_filter('name', "=", name)
    next_item = query.fetch()
    subscription_id = next_item.key
    client.delete(subscription_id)
    return subscription_id


if __name__ == "__main__":
    import datetime
    create(
        space="spaces/i2uCdgAAAAE",
        feed="https://www.reddit.com/r/news/.rss",
        name="Reddit News",
        creator="orix.auyeung@hkmci.com",
        timestamp=str(datetime.datetime.now())
    )
