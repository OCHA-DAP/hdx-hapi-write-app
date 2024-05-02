from datetime import datetime

data_patch = [
    dict(

        patch_sequence_number=1,
        commit_hash='66e7e589a1224a1832ba7360817dda7a7d9313cf',
        commit_date=datetime(2023, 1, 1),
        patch_path='2024/01/hapi_patch_1_hno.json',
        patch_target='humanitarian_needs',
        patch_hash='66e7e589a1224a1832ba7360817dda7a7d9313dg',
        patch_permalink_url='https://github.com/OCHA-DAP/hapi-patch-repo/blob/66e7e589a1224a1832ba7360817dda7a7d9313cf/2024/01/hapi_patch_1_hno.json',
        state='executed',
        execution_date=datetime(2023, 1, 2),
    ),
    dict(
        patch_sequence_number=2,
        commit_hash='554f18a92cf6a23a14e0f29356a6dec150f651ff',
        commit_date=datetime(2023, 1, 2),
        patch_path='2024/01/hapi_patch_2_hno.json',
        patch_target='humanitarian_needs',
        patch_hash='554f18a92cf6a23a14e0f29356a6dec150f651gg',
        patch_permalink_url='https://github.com/OCHA-DAP/hapi-patch-repo/blob/554f18a92cf6a23a14e0f29356a6dec150f651ff/2024/01/hapi_patch_2_hno.json',
        state='failed',
        execution_date=datetime(2023, 1, 3),
    ),
    dict(
        patch_sequence_number=3,
        commit_hash='35ea27da009e5add8d8d227e02fd2c4bbcc84b76',
        commit_date=datetime(2023, 1, 3),
        patch_path='2024/01/hapi_patch_3_hno.json',
        patch_target='humanitarian_needs',
        patch_hash='554f18a92cf6a23a14e0f29356a6dec150f65187',
        patch_permalink_url='https://github.com/OCHA-DAP/hapi-patch-repo/blob/35ea27da009e5add8d8d227e02fd2c4bbcc84b76/2024/01/hapi_patch_3_hno.json',
        state='discovered',
        execution_date=None,
    ),
]
