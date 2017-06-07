auth = dict(
    type='object',
    properties=dict(
        indentity=dict(
            type='object',
            properties=dict(
                methods=dict(
                    type='array',
                    items=dict(type='string')
                    ),
                password=dict(
                    type='object',
                    properties=dict(
                        user=dict(
                            type='object',
                            propoerties=dict(
                                username=dict(type="string"),
                                password=dict(type="string")
                                )
                            )
                        )
                    )
                ),
            required=['methods']
            )
        ),
    required=['identity']
    )


token = dict(
    type='object',
    properties=dict(
        methods=dict(
            type='array',
            items=dict(type='string')
            ),
        id=dict(type='string'),
        user=dict(
            type='object',
            properties=dict(
                id=dict(type='string'),
                username=dict(type='string'),
                )
            ),
        issued_at=dict(type='datetime'),
        expires_at=dict(type='datetime'),
        )
    )

