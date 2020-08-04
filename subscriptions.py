import hashlib

from google.cloud import datastore

client = datastore.Client()

kind = 'feedSubscriptions'


def _get_all_subscription_in_room(space):
    query = client.query(kind=kind)
    query.add_filter('space', '=', space)
    return list(query.fetch())


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
    return subscription_key


def list_all(space):
    subscriptions = _get_all_subscription_in_room(space)
    return subscriptions


def delete_all(space):
    subscriptions = _get_all_subscription_in_room(space)
    client.delete_multi([subscription.key for subscription in subscriptions])


def remove_by_name(space, name):
    query = client.query(kind=kind)
    query.add_filter('space', '=', space)
    query.add_filter('name', "=", name)
    first_item = list(query.fetch())[0]
    key = first_item.key
    client.delete(key)
    return key
