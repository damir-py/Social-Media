# from django.test import TestCase

posts = [
    {
        'id': 1,
        'title': 'a'
    },
    {
        'id': 2,
        'title': 'b'
    },
    {
        'id': 3,
        'title': 'c'
    },
    {
        'id': 4,
        'title': 'd'
    },
]

comments = [
    {
        'post_id': 1,
        'message': 'A'
    },
    {
        'post_id': 1,
        'message': 'B'
    },
    {
        'post_id': 2,
        'message': 'A'
    },
    {
        'post_id': 3,
        'message': 'A'
    },
    {
        'post_id': 4,
        'message': 'A'
    },
    {
        'post_id': 4,
        'message': 'A'
    },
    {
        'post_id': 4,
        'message': 'A'
    },
]


def func(post):
    post['comments'] = list(filter(lambda c: c['post_id'] == post['id'], comments))
    return post


posts = map(func, posts)
# for post in posts:
#     post['comments'] = list(filter(lambda comment: comment['post_id'] == post['id'], comments))

for i in posts:
    print(i)

result = [
    {
        'id': 1,
        'title': 'a',
        'comments': [
            {
                'post_id': 1,
                'message': 'A'
            },
            {
                'post_id': 1,
                'message': 'B'
            },
        ]
    },
    {
        'id': 2,
        'title': 'b',
        'comments': [
            {
                'post_id': 2,
                'message': 'A'
            }
        ]
    },
    {
        'id': 3,
        'title': 'c',
        'comments': [
            {
                'post_id': 3,
                'message': 'A'
            },
        ]
    },
    {
        'id': 4,
        'title': 'd',
        'comments': [
            {
                'post_id': 4,
                'message': 'A'
            },
            {
                'post_id': 4,
                'message': 'A'
            },
            {
                'post_id': 4,
                'message': 'A'
            },
        ]
    },
]
