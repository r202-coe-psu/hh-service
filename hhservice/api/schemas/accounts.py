register = dict(
    type='object',
    properties=dict(
        user=dict(
            type='object',
            properties=dict(
                username=dict(type='string', minimum=3),
                password=dict(type='string', minimum=6),
                email=dict(type='string', format='email'),
                first_name=dict(type='string', minimum=2),
                last_name=dict(type='string', minimum=2)
                ),
            required=['username', 'password', 'email',
                'first_name', 'last_name']
            )
        ),
    required=['user']
    )

