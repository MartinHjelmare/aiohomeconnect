# Changelog

## v0.12.1 (2025-01-29)

### Bug fixes

* Use `raw_key` for the correct dataclasses for programs (#51) ([`a489f6e`](https://github.com/MartinHjelmare/aiohomeconnect/commit/a489f6eaaeeed7b0da8e9f6a8f5d676cbcb899d4))

## v0.12.0 (2025-01-29)

### Features

* Add `raw_key` field (#50) ([`d7ed726`](https://github.com/MartinHjelmare/aiohomeconnect/commit/d7ed72636a2af53f3a7ced3f6f477e5e20d27ba0))

### Chores

* Update dependency pytest-asyncio to v0.25.3 ([`28fd9f0`](https://github.com/MartinHjelmare/aiohomeconnect/commit/28fd9f0df2cedf130341656bb48ac7c3514b945a))
* Update pre-commit hook codespell-project/codespell to v2.4.1 ([`e65ad35`](https://github.com/MartinHjelmare/aiohomeconnect/commit/e65ad35c777b562920008dbbee663d45e7485641))
* Update dependency codespell to v2.4.1 ([`3606b99`](https://github.com/MartinHjelmare/aiohomeconnect/commit/3606b99e5b420d33241460f73764c4377789189b))
* Update dependency authlib to v1.4.1 ([`c796891`](https://github.com/MartinHjelmare/aiohomeconnect/commit/c7968915898c90bbbbbe57a9c388ea00d819f937))
* Update pre-commit hook commitizen-tools/commitizen to v4.1.1 ([`9a72358`](https://github.com/MartinHjelmare/aiohomeconnect/commit/9a723584f300fcd1ff0681e3011e2fc195b71a1e))
* Update python-semantic-release/python-semantic-release action to v9.17.0 ([`9e4210f`](https://github.com/MartinHjelmare/aiohomeconnect/commit/9e4210f34a85a9a3079147024c16cf8273e9f617))
* Update dependency python-semantic-release to v9.17.0 ([`5749354`](https://github.com/MartinHjelmare/aiohomeconnect/commit/57493546d8cc22df2d02af7c0aae4e72e57e8b5d))
* Update renovate semantic commit strategy (#49) ([`5bb49e7`](https://github.com/MartinHjelmare/aiohomeconnect/commit/5bb49e785498b5912a6ea70e26c0018801aeb0d1))

## v0.11.4 (2025-01-25)

### Bug fixes

* Ignore `none` values at models used at `put` requests (#48) ([`6d8000f`](https://github.com/MartinHjelmare/aiohomeconnect/commit/6d8000f99044a704274394cb097232943609d165))

### Chores

* Update pre-commit hook astral-sh/ruff-pre-commit to v0.9.3 ([`058f5c1`](https://github.com/MartinHjelmare/aiohomeconnect/commit/058f5c1a4a05460703e9010dc5f5e752d696cd29))

## v0.11.3 (2025-01-24)

### Bug fixes

* Update dependency fastapi to v0.115.7 ([`9979e6d`](https://github.com/MartinHjelmare/aiohomeconnect/commit/9979e6dddcd49da9870e9a746d2a298d5bc36349))

### Chores

* Update dependency ruff to v0.9.3 ([`d860e20`](https://github.com/MartinHjelmare/aiohomeconnect/commit/d860e20f91700fea39adf4547f4b08483bbf3aec))
* Update pre-commit hook codespell-project/codespell to v2.4.0 ([`808d4ce`](https://github.com/MartinHjelmare/aiohomeconnect/commit/808d4ced4447c413cddd1366481566f4d302e6cf))
* Update dependency codespell to v2.4.0 ([`a2ae0a8`](https://github.com/MartinHjelmare/aiohomeconnect/commit/a2ae0a85b4c153918feb62df66146113a8da88c5))
* Update dependency pre-commit to v4.1.0 ([`9600c8f`](https://github.com/MartinHjelmare/aiohomeconnect/commit/9600c8f579305ce86129a87194b83d7a5f0fa4c1))
* Update dependency ruff to v0.9.2 (#47) ([`10032bb`](https://github.com/MartinHjelmare/aiohomeconnect/commit/10032bbdb5ea9fa9187a95f8b766b8eb5f45d784))
* Update pre-commit hook astral-sh/ruff-pre-commit to v0.9.2 ([`bcd43a5`](https://github.com/MartinHjelmare/aiohomeconnect/commit/bcd43a5c38970ce6abf423d6e6b81ec6f83647dc))

## v0.11.2 (2025-01-17)

### Bug fixes

* Fix requests that have a body (#46) ([`13134f4`](https://github.com/MartinHjelmare/aiohomeconnect/commit/13134f4bb3d5e6409120958ef79d2e6e579af52d))

## v0.11.1 (2025-01-16)

### Bug fixes

* Raise exception only on error request (#45) ([`e5479a7`](https://github.com/MartinHjelmare/aiohomeconnect/commit/e5479a7577d208a0ed6863a083f6e689eb875b96))

### Chores

* Update wagoid/commitlint-github-action action to v6.2.1 ([`c897247`](https://github.com/MartinHjelmare/aiohomeconnect/commit/c897247417605b475d4d0537048b1323c6c6a96b))

## v0.11.0 (2025-01-14)

### Features

* Reference options, settings, and status enum keys at events enum (#43) ([`e391340`](https://github.com/MartinHjelmare/aiohomeconnect/commit/e391340c3af2c3545f5d6f404784e9e0a3ba7d1a))

## v0.10.0 (2025-01-13)

### Features

* Raise exceptions on http errors (#44) ([`112cd75`](https://github.com/MartinHjelmare/aiohomeconnect/commit/112cd75094285117201d0672072ec61d0ffcd7a5))

### Chores

* Update python-semantic-release/python-semantic-release action to v9.16.1 ([`6848225`](https://github.com/MartinHjelmare/aiohomeconnect/commit/6848225337fd05d215e1d1dbcf7a900b65da7bbc))
* Update dependency python-semantic-release to v9.16.1 ([`ab274a6`](https://github.com/MartinHjelmare/aiohomeconnect/commit/ab274a639521e4907ab1b808f6093cfc6df1bdd5))
* Update python-semantic-release/python-semantic-release action to v9.16.0 ([`a5245d0`](https://github.com/MartinHjelmare/aiohomeconnect/commit/a5245d02202f2c5e4ffb9971619faeab30683146))
* Update dependency python-semantic-release to v9.16.0 ([`d005128`](https://github.com/MartinHjelmare/aiohomeconnect/commit/d005128e6a4fca7533a269179ec63aff179ae15e))
* Update pre-commit hook astral-sh/ruff-pre-commit to v0.9.1 ([`39bcea1`](https://github.com/MartinHjelmare/aiohomeconnect/commit/39bcea1c9c9918bf982d8e20e1d05470d42fef12))
* Update dependency ruff to v0.9.1 ([`87d73d9`](https://github.com/MartinHjelmare/aiohomeconnect/commit/87d73d9b4bc91837f3e4e4bdbac594deda6cf4dd))

## v0.9.0 (2025-01-10)

### Features

* Support unknown enum values (#41) ([`efced94`](https://github.com/MartinHjelmare/aiohomeconnect/commit/efced94961f56e1f6621c587113f18d067231158))

## v0.8.0 (2025-01-09)

### Chores

* Update pre-commit hook astral-sh/ruff-pre-commit to v0.9.0 (#42) ([`edaca49`](https://github.com/MartinHjelmare/aiohomeconnect/commit/edaca49ac00e64a11924d41b998f7ca1d5f18975))
* Update dependency ruff to ^0.9.0 ([`100c5a2`](https://github.com/MartinHjelmare/aiohomeconnect/commit/100c5a2c0df4a5140ab0aace60d512b37878c201))
* Update dependency pytest-asyncio to v0.25.2 ([`58b57ea`](https://github.com/MartinHjelmare/aiohomeconnect/commit/58b57ea933a8e730a2adc10f420a5e18146fc4f7))

### Features

* Complete string enumerations and fix names (#40) ([`b92e281`](https://github.com/MartinHjelmare/aiohomeconnect/commit/b92e2818623a4d72539eb362cbe5721d14d43e31))

## v0.7.5 (2025-01-06)

### Bug fixes

* Set default values for optional model attributes (#37) ([`bb2744a`](https://github.com/MartinHjelmare/aiohomeconnect/commit/bb2744a165fbcab5e0de9a4c58e10e7d5f6a0a66))

## v0.7.4 (2025-01-06)

### Bug fixes

* Home appliance model (#36) ([`5cd6e06`](https://github.com/MartinHjelmare/aiohomeconnect/commit/5cd6e064673bff8df9c9fc5ec4f8259682d2b58e))

### Chores

* Update pre-commit hook astral-sh/ruff-pre-commit to v0.8.6 ([`14726f3`](https://github.com/MartinHjelmare/aiohomeconnect/commit/14726f30d01dc80195f6176c76a365e52b48c5f5))
* Update dependency ruff to v0.8.6 ([`da2e644`](https://github.com/MartinHjelmare/aiohomeconnect/commit/da2e6449100d96a988bc98855aa678a993a188f8))
* Update pre-commit hook astral-sh/ruff-pre-commit to v0.8.5 ([`ea11e0e`](https://github.com/MartinHjelmare/aiohomeconnect/commit/ea11e0e7671be32830a110f227d6926fb2de1884))
* Update dependency ruff to v0.8.5 ([`3f08d0f`](https://github.com/MartinHjelmare/aiohomeconnect/commit/3f08d0f23d117af9644c9b8cf2ebe843d02ea1a6))
* Update dependency pytest-asyncio to v0.25.1 ([`abce45b`](https://github.com/MartinHjelmare/aiohomeconnect/commit/abce45b406c4de0e445bcb6b44a27a0cb3d3304a))
* Update dependency mypy to v1.14.1 ([`94db878`](https://github.com/MartinHjelmare/aiohomeconnect/commit/94db87891aa63851967e2c0c107e95c25c4e92f6))
* Update dependency mypy to v1.14.0 ([`4bd28fc`](https://github.com/MartinHjelmare/aiohomeconnect/commit/4bd28fcedaba29caf288de2446417ed65d26f9bc))

## v0.7.3 (2024-12-20)

### Bug fixes

* Update dependency authlib to v1.4.0 ([`be1d018`](https://github.com/MartinHjelmare/aiohomeconnect/commit/be1d018b1b21d10ef91d438ec65663da7bad9447))

### Chores

* Update pre-commit hook astral-sh/ruff-pre-commit to v0.8.4 ([`df362f2`](https://github.com/MartinHjelmare/aiohomeconnect/commit/df362f2415eb7564fbd0300f9e08a490bf224cec))
* Update dependency ruff to v0.8.4 ([`272602a`](https://github.com/MartinHjelmare/aiohomeconnect/commit/272602a153cae7cae123296962b5678ec2ca11c7))
* Update wagoid/commitlint-github-action action to v6.2.0 ([`7e07707`](https://github.com/MartinHjelmare/aiohomeconnect/commit/7e077072a47e4f198bebeb990a8f5c2cba88924c))
* Update python-semantic-release/python-semantic-release action to v9.15.2 ([`c342360`](https://github.com/MartinHjelmare/aiohomeconnect/commit/c342360d645f9011c6a927217379b3d63d3ffc9c))
* Update dependency python-semantic-release to v9.15.2 ([`415d88d`](https://github.com/MartinHjelmare/aiohomeconnect/commit/415d88d4c0fc725b8cacbfb453f2483105430a03))

## v0.7.2 (2024-12-15)

### Bug fixes

* Update dependency uvicorn to ^0.34.0 ([`a36533c`](https://github.com/MartinHjelmare/aiohomeconnect/commit/a36533c29baa1786c98e8d00cb145ad4be1c131f))

## v0.7.1 (2024-12-14)

### Bug fixes

* Update dependency uvicorn to ^0.33.0 ([`0f91cc5`](https://github.com/MartinHjelmare/aiohomeconnect/commit/0f91cc5f8c37027469fd7b0ded6e35489a825698))

### Chores

* Update dependency pytest-asyncio to ^0.25.0 ([`94b4cbc`](https://github.com/MartinHjelmare/aiohomeconnect/commit/94b4cbcfdc3ebc8095b22e26f9a867def4bd4394))
* Update pre-commit hook astral-sh/ruff-pre-commit to v0.8.3 ([`46ae9e2`](https://github.com/MartinHjelmare/aiohomeconnect/commit/46ae9e217f29df0259ca5738d8aec23eee91dc5c))
* Update dependency ruff to v0.8.3 ([`15c7b6e`](https://github.com/MartinHjelmare/aiohomeconnect/commit/15c7b6ec8d2fec72038bb1e7f3c462285cc77204))

## v0.7.0 (2024-12-12)

### Features

* Add sse streams (#34) ([`36a53a4`](https://github.com/MartinHjelmare/aiohomeconnect/commit/36a53a4eedac701b359857f1f75475fcec5547c3))

## v0.6.4 (2024-12-07)

### Bug fixes

* Update dependency httpx to v0.28.1 ([`8939e1c`](https://github.com/MartinHjelmare/aiohomeconnect/commit/8939e1c7324683a520c79b2f34227875825bd697))

### Chores

* Update pre-commit hook commitizen-tools/commitizen to v4.1.0 ([`3d56bbd`](https://github.com/MartinHjelmare/aiohomeconnect/commit/3d56bbd01cc16a6c32b929cb0773a0004eb19fd9))
* Update pre-commit hook python-poetry/poetry to v1.8.5 ([`ae327a8`](https://github.com/MartinHjelmare/aiohomeconnect/commit/ae327a8adf546a7cdb69dcb425bc2a1045cea640))
* Update pre-commit hook astral-sh/ruff-pre-commit to v0.8.2 ([`422fd30`](https://github.com/MartinHjelmare/aiohomeconnect/commit/422fd3004a0c0e5ab00022140e09fa8de6e957f2))
* Update dependency ruff to v0.8.2 ([`a531dbd`](https://github.com/MartinHjelmare/aiohomeconnect/commit/a531dbdfe321aea3b9fb8f74e56a7cee2e807798))

## v0.6.3 (2024-12-04)

### Bug fixes

* Update dependency typer to v0.15.1 ([`5fd604d`](https://github.com/MartinHjelmare/aiohomeconnect/commit/5fd604d740bea69d2c7166033795471ac6507b2d))

### Chores

* Update actions/attest-build-provenance action to v2 (#32) ([`e2a2a57`](https://github.com/MartinHjelmare/aiohomeconnect/commit/e2a2a575fb99c684ec7e57c39e040679c064a200))

## v0.6.2 (2024-12-04)

### Bug fixes

* Update dependency fastapi to v0.115.6 ([`984e2eb`](https://github.com/MartinHjelmare/aiohomeconnect/commit/984e2ebc10baee0fef5189b9b5b8c9d7ff61eb8f))

## v0.6.1 (2024-12-03)

### Bug fixes

* Update dependency typer to ^0.15.0 ([`ff03685`](https://github.com/MartinHjelmare/aiohomeconnect/commit/ff03685e24742ee80cfd085b761bd0d5102d2beb))

### Chores

* Update python-semantic-release/python-semantic-release action to v9.15.1 ([`9180351`](https://github.com/MartinHjelmare/aiohomeconnect/commit/9180351ee274b76984219aa4a15aed4f20700e59))
* Update dependency python-semantic-release to v9.15.1 ([`fb7adcd`](https://github.com/MartinHjelmare/aiohomeconnect/commit/fb7adcdf1fdf4b7dbfef56710f87e7d3049d5ae2))
* Update python-semantic-release/python-semantic-release action to v9.15.0 ([`34df80b`](https://github.com/MartinHjelmare/aiohomeconnect/commit/34df80b88e2fdea9cdf4eca158f418244454f61b))
* Update dependency python-semantic-release to v9.15.0 ([`e3b1677`](https://github.com/MartinHjelmare/aiohomeconnect/commit/e3b1677ce3fbf17418ba1017c2ce135a2285f4c6))
* Update dependency pytest to v8.3.4 ([`061fe78`](https://github.com/MartinHjelmare/aiohomeconnect/commit/061fe78e252f98b2fb0138a87385c1dd0275b732))

## v0.6.0 (2024-11-30)

### Features

* Add dishwasher keys (#31) ([`496079f`](https://github.com/MartinHjelmare/aiohomeconnect/commit/496079fa4cc6a5e7e6d207710cc24d9a94e6c960))

### Chores

* Update pre-commit hook astral-sh/ruff-pre-commit to v0.8.1 ([`ed33502`](https://github.com/MartinHjelmare/aiohomeconnect/commit/ed3350208e9000b8bbb3e413c5f9a0faa2290697))

## v0.5.2 (2024-11-29)

### Bug fixes

* Update httpx ([`a3cc541`](https://github.com/MartinHjelmare/aiohomeconnect/commit/a3cc541b5e1bbfad93f72c7d1633d0d05c908c32))

### Chores

* Add httpx renovate group (#30) ([`1b94f22`](https://github.com/MartinHjelmare/aiohomeconnect/commit/1b94f22136321530a3b857005360915ba281444e))
* Update dependency ruff to v0.8.1 ([`bb22973`](https://github.com/MartinHjelmare/aiohomeconnect/commit/bb229732a862642cdc4a20f22d541fa26be6412a))

## v0.5.1 (2024-11-29)

### Bug fixes

* Update dependency typer to ^0.14.0 ([`f1fd272`](https://github.com/MartinHjelmare/aiohomeconnect/commit/f1fd272aceab684fd1bdee711077108cbcc0df3f))

### Chores

* Update pre-commit hook commitizen-tools/commitizen to v4 (#27) ([`c308a23`](https://github.com/MartinHjelmare/aiohomeconnect/commit/c308a233af16c5d4c0cf95cfbd4382bdc97dca1e))

## v0.5.0 (2024-11-25)

### Features

* Add coffee machine keys (#26) ([`d002752`](https://github.com/MartinHjelmare/aiohomeconnect/commit/d00275212d5662f6f1b50c5e10ed370d2a90e8ea))

## v0.4.0 (2024-11-24)

### Features

* Finish event keys (#25) ([`3b2d74c`](https://github.com/MartinHjelmare/aiohomeconnect/commit/3b2d74cc32571d8462be7a14e2eda65bc7f0f256))

## v0.3.0 (2024-11-24)

### Features

* Add model foundation (#24) ([`722f614`](https://github.com/MartinHjelmare/aiohomeconnect/commit/722f61472d375debaf73c5fb40937e1495929fac))

## v0.2.13 (2024-11-23)

### Bug fixes

* Update dependency mashumaro to v3.15 ([`6720330`](https://github.com/MartinHjelmare/aiohomeconnect/commit/6720330a0127ae4315e697c3a0354246c1e31bea))

### Chores

* Add dev deps (#20) ([`c34be68`](https://github.com/MartinHjelmare/aiohomeconnect/commit/c34be68a31d52c2a87d73e2eacd01bc88eea43cd))
* Update pre-commit stages (#19) ([`b116296`](https://github.com/MartinHjelmare/aiohomeconnect/commit/b1162968425a858ab80119f7bede09af554e0e1f))
* Update pre-commit hook astral-sh/ruff-pre-commit to v0.8.0 (#18) ([`1a47670`](https://github.com/MartinHjelmare/aiohomeconnect/commit/1a47670cd3a91b39e98c7fd13cff574de2d624d7))
* Update dependency ruff to ^0.8.0 ([`594fcdb`](https://github.com/MartinHjelmare/aiohomeconnect/commit/594fcdbd83f09ae264af2c3f1ceef9b95ce7073e))

## v0.2.12 (2024-11-21)

### Bug fixes

* Update dependency uvicorn to v0.32.1 ([`d9b8b88`](https://github.com/MartinHjelmare/aiohomeconnect/commit/d9b8b881ad309d7a5f622d5741fab340930d11a4))

## v0.2.11 (2024-11-19)

### Bug fixes

* Update dependency typer to v0.13.1 ([`1c96fba`](https://github.com/MartinHjelmare/aiohomeconnect/commit/1c96fbad25a86f3381d00a619ddb655a31d72ed1))

### Chores

* Update dependency pytest-httpx to ^0.34.0 ([`2b6fc43`](https://github.com/MartinHjelmare/aiohomeconnect/commit/2b6fc432aa4a6d9272babb73b6dc8bf172e3dda1))
* Update pre-commit hook commitizen-tools/commitizen to v3.31.0 ([`1d21e85`](https://github.com/MartinHjelmare/aiohomeconnect/commit/1d21e85cad2ac5ce18c7f33071f0460149451669))
* Update pre-commit hook astral-sh/ruff-pre-commit to v0.7.4 ([`921b415`](https://github.com/MartinHjelmare/aiohomeconnect/commit/921b4152a46c0be9ffef134f71bed07cf99c5d47))
* Update dependency ruff to v0.7.4 ([`64d8c83`](https://github.com/MartinHjelmare/aiohomeconnect/commit/64d8c8352d4bbad8ed918a715ae241d12e7a5de2))
* Update codecov/codecov-action action to v5 (#17) ([`2aaffe9`](https://github.com/MartinHjelmare/aiohomeconnect/commit/2aaffe9bff97868ab6d4714c089964e3357ad933))

## v0.2.10 (2024-11-12)

### Bug fixes

* Update dependency fastapi to v0.115.5 ([`c07099b`](https://github.com/MartinHjelmare/aiohomeconnect/commit/c07099b8797116ec6987fe1e5d97c8114018c7ba))

### Chores

* Update python-semantic-release/python-semantic-release action to v9.14.0 ([`3b53c0e`](https://github.com/MartinHjelmare/aiohomeconnect/commit/3b53c0e76bdb6e3e98cfafcaab510375b3ee0df8))
* Update python-semantic-release/python-semantic-release action to v9.13.0 ([`30ec017`](https://github.com/MartinHjelmare/aiohomeconnect/commit/30ec0172389ecc80056f1c00cfa5f2755cf50111))
* Update pre-commit hook commitizen-tools/commitizen to v3.30.1 ([`f98997e`](https://github.com/MartinHjelmare/aiohomeconnect/commit/f98997e3cca18d7dddec3302b85d4658628de7be))
* Update pre-commit hook astral-sh/ruff-pre-commit to v0.7.3 ([`9a7579a`](https://github.com/MartinHjelmare/aiohomeconnect/commit/9a7579a73d5bfe514a477dbf2f63b95e23a74784))
* Update dependency ruff to v0.7.3 ([`d15fd14`](https://github.com/MartinHjelmare/aiohomeconnect/commit/d15fd1402b81b99edc0ded4259749d7ef3d30481))
* Adjust typer deps (#16) ([`8704e1f`](https://github.com/MartinHjelmare/aiohomeconnect/commit/8704e1fab551ba41e7f40fb315426074800227b7))

## v0.2.9 (2024-11-08)

### Bug fixes

* Update dependency typer to ^0.13.0 ([`b450fda`](https://github.com/MartinHjelmare/aiohomeconnect/commit/b450fda42a96b21c39b31e45798e04f822686d12))

### Chores

* Update python-semantic-release/python-semantic-release action to v9.12.2 ([`01b7772`](https://github.com/MartinHjelmare/aiohomeconnect/commit/01b7772ad4f29c7bbb647475a64f053bf53393ea))
* Update python-semantic-release/python-semantic-release action to v9.12.1 ([`e301ce5`](https://github.com/MartinHjelmare/aiohomeconnect/commit/e301ce54433b33a5bbb6fe283d30f5081250dea3))
* Update pre-commit hook astral-sh/ruff-pre-commit to v0.7.2 (#15) ([`217c40e`](https://github.com/MartinHjelmare/aiohomeconnect/commit/217c40e17d2f7e15a3f26b1516f9ddbf531c03cc))

## v0.2.8 (2024-11-01)

### Bug fixes

* Update dependency rich to v13.9.4 ([`60bc03b`](https://github.com/MartinHjelmare/aiohomeconnect/commit/60bc03b271a53df28fd37145f64846ea3d97640b))

### Chores

* Update dependency ruff to v0.7.2 ([`1c31577`](https://github.com/MartinHjelmare/aiohomeconnect/commit/1c31577a61e5e2d322364f918a2b078d7504ebb3))
* Update dependency pytest-cov to v6 (#14) ([`9c633cb`](https://github.com/MartinHjelmare/aiohomeconnect/commit/9c633cb4fd75e331a785ec6febc7a7b07baf0852))
* Update dependency pytest-httpx to ^0.33.0 ([`b1dca5e`](https://github.com/MartinHjelmare/aiohomeconnect/commit/b1dca5e44e28d0a921f950803c24170b988f5507))

## v0.2.7 (2024-10-28)

### Bug fixes

* Update dependency fastapi to v0.115.4 ([`6e546d9`](https://github.com/MartinHjelmare/aiohomeconnect/commit/6e546d9be4aa24c51d01194452f1121ed7f414a3))

### Chores

* Update pre-commit hook astral-sh/ruff-pre-commit to v0.7.1 ([`76facd6`](https://github.com/MartinHjelmare/aiohomeconnect/commit/76facd6ddd11aea4746f971280178d23457ef43e))
* Update dependency ruff to v0.7.1 ([`acd0867`](https://github.com/MartinHjelmare/aiohomeconnect/commit/acd086784f91461cb97a1c563e9aa303571e413a))

## v0.2.6 (2024-10-24)

### Bug fixes

* Update dependency mashumaro to v3.14 ([`0ee6d7f`](https://github.com/MartinHjelmare/aiohomeconnect/commit/0ee6d7fe3e25ce6896b0783d03ef780aa82a555e))

### Chores

* Update pre-commit hook commitizen-tools/commitizen to v3.30.0 ([`88e9197`](https://github.com/MartinHjelmare/aiohomeconnect/commit/88e9197767ad566b9ec7e6a3310d40038ecaf919))
* Update dependency mypy to v1.13.0 ([`2e7a4ca`](https://github.com/MartinHjelmare/aiohomeconnect/commit/2e7a4ca4025032739b077e03b01f07438a001ddf))

## v0.2.5 (2024-10-22)

### Bug fixes

* Update dependency rich to v13.9.3 ([`8bb77ee`](https://github.com/MartinHjelmare/aiohomeconnect/commit/8bb77ee3893eb6f1c7d246fbda161ac032dae762))

## v0.2.4 (2024-10-22)

### Bug fixes

* Update dependency fastapi to v0.115.3 ([`f6a6283`](https://github.com/MartinHjelmare/aiohomeconnect/commit/f6a6283b22582e2e0e4556f032415b132f2a1794))

### Chores

* Update dependency mypy to v1.12.1 ([`df22023`](https://github.com/MartinHjelmare/aiohomeconnect/commit/df22023a7c80d43176b43fb4b088233b4eb816e4))
* Update dependency copier to v9.4.1 ([`c17118c`](https://github.com/MartinHjelmare/aiohomeconnect/commit/c17118c2af8c2d372140ff06d5871c85bdfa09b2))
* Update python-semantic-release/python-semantic-release action to v9.12.0 ([`88095ce`](https://github.com/MartinHjelmare/aiohomeconnect/commit/88095ce8c89e8dc72c498b1e5710a8b6022af0b4))
* Update pre-commit hook astral-sh/ruff-pre-commit to v0.7.0 ([`17206d5`](https://github.com/MartinHjelmare/aiohomeconnect/commit/17206d50f5b5cc38fe556aa6e6c579ae9f89cde1))
* Update dependency ruff to ^0.7.0 ([`9d55d9d`](https://github.com/MartinHjelmare/aiohomeconnect/commit/9d55d9d8677d21c226ab9e9460a637dc32c44fe5))

## v0.2.3 (2024-10-15)

### Bug fixes

* Update dependency uvicorn to ^0.32.0 ([`49d3f81`](https://github.com/MartinHjelmare/aiohomeconnect/commit/49d3f81b3e0e488105f7a7f5b8af9307b04311bf))

### Chores

* Update dependency copier to v9.4.0 ([`6a2496b`](https://github.com/MartinHjelmare/aiohomeconnect/commit/6a2496b551991a266fb46253c83d4eecfb3ce1a3))
* Update python-semantic-release/python-semantic-release action to v9.11.1 ([`418cf71`](https://github.com/MartinHjelmare/aiohomeconnect/commit/418cf71033f8adb0dd542440e5ace8d85e7394bf))
* Update dependency mypy to v1.12.0 ([`5f288af`](https://github.com/MartinHjelmare/aiohomeconnect/commit/5f288af13a3a7fcf14d45613ef10b5458ca3a443))
* Update pre-commit hook python-poetry/poetry to v1.8.4 ([`5fad5d8`](https://github.com/MartinHjelmare/aiohomeconnect/commit/5fad5d8fbfe318802e86dce5784a4ffc65d2a24d))
* Update dependency sphinx to v8.1.3 ([`6bebda6`](https://github.com/MartinHjelmare/aiohomeconnect/commit/6bebda660dd85b1b237cc974a4d4a757c73c891d))
* Update python-semantic-release/python-semantic-release action to v9.11.0 ([`410afec`](https://github.com/MartinHjelmare/aiohomeconnect/commit/410afec9cbd50f4a61999fc44c3b98f2d8c45dc1))
* Update dependency sphinx to v8.1.2 ([`8a7f0f9`](https://github.com/MartinHjelmare/aiohomeconnect/commit/8a7f0f96ef37d6111732a3d6306fa850bff7f212))

## v0.2.2 (2024-10-12)

### Bug fixes

* Update dependency fastapi to v0.115.2 ([`ccb61a0`](https://github.com/MartinHjelmare/aiohomeconnect/commit/ccb61a0a0a2afbcf27d75bb0ba8f6d7ef4f743c5))

### Chores

* Update dependency sphinx to v8.1.1 ([`7b9f86b`](https://github.com/MartinHjelmare/aiohomeconnect/commit/7b9f86b31579a842a41d97044f6e4fd1c73ea39e))
* Update dependency sphinx to v8.1.0 ([`61ade9b`](https://github.com/MartinHjelmare/aiohomeconnect/commit/61ade9b7eda485a093095af40db2e5b7dc441f56))
* Update python-semantic-release/python-semantic-release action to v9.10.1 ([`7242c58`](https://github.com/MartinHjelmare/aiohomeconnect/commit/7242c58d38312a180632011063f0cddd9f8f31b1))

## v0.2.1 (2024-10-10)

### Bug fixes

* Update dependency uvicorn to v0.31.1 ([`285c771`](https://github.com/MartinHjelmare/aiohomeconnect/commit/285c771dbc0c76f47a01dfd05c64b435a293ef1c))

### Chores

* Update dependency pre-commit to v4.0.1 ([`d71f6af`](https://github.com/MartinHjelmare/aiohomeconnect/commit/d71f6af97da0c1c108786e0747962707a99d025e))
* Clean up dummy modules (#13) ([`6fdbaa8`](https://github.com/MartinHjelmare/aiohomeconnect/commit/6fdbaa8b219137c8ed952df89c5c88033d053b8e))
* Update python-semantic-release/python-semantic-release action to v9.10.0 ([`a53ec37`](https://github.com/MartinHjelmare/aiohomeconnect/commit/a53ec37780e021f35fa66b0f10c99fd20408d87d))

## v0.2.0 (2024-10-07)

### Features

* Add swagger parser (#12) ([`aefbefa`](https://github.com/MartinHjelmare/aiohomeconnect/commit/aefbefa9378c7a505e1fca93c28dce69a3a9a46f))

### Chores

* Update pre-commit hook pre-commit/pre-commit-hooks to v5 (#11) ([`2efcc82`](https://github.com/MartinHjelmare/aiohomeconnect/commit/2efcc82620650b6587f4e4acdb7a1463d5c2c6df))
* Update dependency pre-commit to v4 (#10) ([`33e1426`](https://github.com/MartinHjelmare/aiohomeconnect/commit/33e14260caa796c97c0f8f4bd44631bb4578d453))
* Update dependency ruff to v0.6.9 ([`1446317`](https://github.com/MartinHjelmare/aiohomeconnect/commit/144631796e6bc3962e6c1b1441f75beac992d843))

## v0.1.9 (2024-10-04)

### Chores

* Update pre-commit hook astral-sh/ruff-pre-commit to v0.6.9 ([`428a634`](https://github.com/MartinHjelmare/aiohomeconnect/commit/428a634b12cc4ffd4b83808c96f00a2edc320636))
* Update dependency sphinx-autobuild to v2024.10.3 ([`15f403e`](https://github.com/MartinHjelmare/aiohomeconnect/commit/15f403e34d41476e4c6380a85266027d2651190b))
* Update dependency sphinx-autobuild to v2024.10.2 ([`ceefac4`](https://github.com/MartinHjelmare/aiohomeconnect/commit/ceefac4357966f54506e6c303b50b7c0d9db158e))

### Bug fixes

* Update dependency rich to v13.9.2 ([`7513478`](https://github.com/MartinHjelmare/aiohomeconnect/commit/751347844d7e32996b6b8ffb7651502fd28f1144))

## v0.1.8 (2024-10-01)

### Bug fixes

* Update dependency rich to v13.9.1 ([`7737f85`](https://github.com/MartinHjelmare/aiohomeconnect/commit/7737f85453212005bb9c55bffdd5a7d131763a7c))

### Chores

* Update python-semantic-release/python-semantic-release action to v9.9.0 ([`b88a3c8`](https://github.com/MartinHjelmare/aiohomeconnect/commit/b88a3c8a61755bd524f7cc0efdfb536dcc75a4f4))

## v0.1.7 (2024-09-28)

### Bug fixes

* Update dependency uvicorn to ^0.31.0 ([`d42aafd`](https://github.com/MartinHjelmare/aiohomeconnect/commit/d42aafdbee1c96658f520cec0a05a2a013750ce7))

### Chores

* Update dependency pytest-httpx to ^0.32.0 ([`3a27f70`](https://github.com/MartinHjelmare/aiohomeconnect/commit/3a27f700fcb18cfc9685f236685b09ce579a2815))
* Update python-semantic-release/python-semantic-release action to v9.8.9 ([`a4e708d`](https://github.com/MartinHjelmare/aiohomeconnect/commit/a4e708daa84fa18ac606a6038e4499aaeebb4a32))
* Update pre-commit hook astral-sh/ruff-pre-commit to v0.6.8 ([`df7f684`](https://github.com/MartinHjelmare/aiohomeconnect/commit/df7f68487fdc04132e352f2aff22ff8456d392aa))
* Update pre-commit hook commitizen-tools/commitizen to v3.29.1 ([`8f22978`](https://github.com/MartinHjelmare/aiohomeconnect/commit/8f2297824873946d4ef46cf7ec2805683ed5d4c0))
* Update dependency ruff to v0.6.8 ([`0d11494`](https://github.com/MartinHjelmare/aiohomeconnect/commit/0d11494953a38baa7a8d87683a35fe4f7100370a))
* Update dependency pytest-httpx to v0.31.2 ([`0d676b9`](https://github.com/MartinHjelmare/aiohomeconnect/commit/0d676b9cd9172c2bdead77c1196a12e6e8448502))
* Update dependency pytest-httpx to v0.31.1 ([`0359b7b`](https://github.com/MartinHjelmare/aiohomeconnect/commit/0359b7b13f465f2ae19c767c7ab447a46babee06))
* Update pre-commit hook astral-sh/ruff-pre-commit to v0.6.7 ([`1fa3351`](https://github.com/MartinHjelmare/aiohomeconnect/commit/1fa3351adf707f38c7b29978310a78bad1616987))
* Update dependency ruff to v0.6.7 ([`1bf695e`](https://github.com/MartinHjelmare/aiohomeconnect/commit/1bf695ec375e015035fddb4fb8df97e2b06314db))
* Fix license identifier (#9) ([`2ef3e5b`](https://github.com/MartinHjelmare/aiohomeconnect/commit/2ef3e5b8fdef4f33cb5f19e54c2f8f2738819662))
* Update dependency pytest-httpx to ^0.31.0 ([`5f2d3a7`](https://github.com/MartinHjelmare/aiohomeconnect/commit/5f2d3a7c6288de47fb7a3cf198222ef91811e234))
* Update pre-commit hook astral-sh/ruff-pre-commit to v0.6.6 ([`235e38a`](https://github.com/MartinHjelmare/aiohomeconnect/commit/235e38a399f61926919884b0c752143793fd8c11))
* Update dependency ruff to v0.6.6 ([`e1d98aa`](https://github.com/MartinHjelmare/aiohomeconnect/commit/e1d98aa001d9536280def603f1055d8d0611771b))
* Update dependency sphinx-autobuild to v2024.9.19 ([`a2f5307`](https://github.com/MartinHjelmare/aiohomeconnect/commit/a2f53070592ea2aede019388482ed335d7d272c2))

## v0.1.6 (2024-09-18)

### Bug fixes

* Update dependency fastapi to ^0.115.0 ([`ddfa69a`](https://github.com/MartinHjelmare/aiohomeconnect/commit/ddfa69a4a03ad2639815dc341637d88cea82d44a))

### Chores

* Update dependency sphinx-autobuild to v2024.9.17 ([`3635697`](https://github.com/MartinHjelmare/aiohomeconnect/commit/36356974a342e8662e7d7f6841850da196c28302))

## v0.1.5 (2024-09-14)

### Bug fixes

* Update dependency fastapi to v0.114.2 ([`d6696fc`](https://github.com/MartinHjelmare/aiohomeconnect/commit/d6696fc00c89a6948349f4102e5066242be8b3ab))

### Chores

* Update pre-commit hook astral-sh/ruff-pre-commit to v0.6.5 ([`6f5e3ca`](https://github.com/MartinHjelmare/aiohomeconnect/commit/6f5e3ca9e7e3c35f1c99252087d2f9c1c86f2837))
* Update dependency ruff to v0.6.5 ([`7d5fe39`](https://github.com/MartinHjelmare/aiohomeconnect/commit/7d5fe3915b7660ceb799c60ab4da8dd9478bb8b7))

## v0.1.4 (2024-09-11)

### Bug fixes

* Update dependency fastapi to v0.114.1 ([`aef28b9`](https://github.com/MartinHjelmare/aiohomeconnect/commit/aef28b92e7ab2db460f9e181cee441c139429112))

## v0.1.3 (2024-09-10)

### Bug fixes

* Update dependency rich to v13.8.1 ([`6a8e428`](https://github.com/MartinHjelmare/aiohomeconnect/commit/6a8e4288887871d8c7ad844b08f5fc13d273b079))

### Chores

* Update dependency pytest to v8.3.3 ([`fbdc52c`](https://github.com/MartinHjelmare/aiohomeconnect/commit/fbdc52c7868a2e4ab93f2d498f3fbeccfe205573))
* Update tiangolo/issue-manager action to v0.5.1 ([`6775064`](https://github.com/MartinHjelmare/aiohomeconnect/commit/6775064fd9ba00b901bf4f105ebd3b1120e1d508))

## v0.1.2 (2024-09-07)

### Bug fixes

* Update dependency fastapi to ^0.114.0 ([`867393c`](https://github.com/MartinHjelmare/aiohomeconnect/commit/867393c0f36fcc581e487616f1d510118ff415a7))

### Chores

* Update dependency ruff to v0.6.4 (#8) ([`61bd08f`](https://github.com/MartinHjelmare/aiohomeconnect/commit/61bd08f1a7d408c7d1bf322bdbc9b67961fc5cd7))
* Update pre-commit hook astral-sh/ruff-pre-commit to v0.6.4 ([`9b907d4`](https://github.com/MartinHjelmare/aiohomeconnect/commit/9b907d472414b5aade39a3a3e65d80c798a0a94d))
* Update wagoid/commitlint-github-action action to v6.1.2 ([`06959f3`](https://github.com/MartinHjelmare/aiohomeconnect/commit/06959f310674a95f737a230df05b4fbf8e5827a0))
* Update dependency sphinx-autobuild to v2024.9.3 ([`537f68d`](https://github.com/MartinHjelmare/aiohomeconnect/commit/537f68d4ed85f6384d8d70c2ba0c5346581a3fec))
* Update python-semantic-release/python-semantic-release action to v9.8.8 ([`856bccb`](https://github.com/MartinHjelmare/aiohomeconnect/commit/856bccbc4d096e977a16e674c5c7657993095bfe))
* Update pre-commit hook astral-sh/ruff-pre-commit to v0.6.3 ([`9dd308e`](https://github.com/MartinHjelmare/aiohomeconnect/commit/9dd308e3d289e8e980294806691d42369875f9e6))
* Update dependency ruff to v0.6.3 ([`6991f91`](https://github.com/MartinHjelmare/aiohomeconnect/commit/6991f91da515c912d437a8762957e6cda3c3d4dc))

## v0.1.1 (2024-08-29)

### Bug fixes

* Update dependency typer to ^0.12.0 ([`b3f841d`](https://github.com/MartinHjelmare/aiohomeconnect/commit/b3f841dabb1e6072d120b78219d16e8f8ae7a827))

### Chores

* Remove unused black dep (#6) ([`c5d39ae`](https://github.com/MartinHjelmare/aiohomeconnect/commit/c5d39aea694828fb09804936c58802be383b77bc))
* Update wagoid/commitlint-github-action action to v6.1.1 ([`76daf53`](https://github.com/MartinHjelmare/aiohomeconnect/commit/76daf531df1283540fa593f2e55f14b6c43041f0))

### Continuous integration

* Add lint pr action (#4) ([`4812082`](https://github.com/MartinHjelmare/aiohomeconnect/commit/48120829b3fbd7eed3759bc37c3cd09fbeba591f))

## v0.1.0 (2024-08-28)

### Chores

* Run copier update (#3) ([`759f302`](https://github.com/MartinHjelmare/aiohomeconnect/commit/759f302a7807cb06702990adbdc7014bbe093379))
* Add dev deps ([`ff7c1ad`](https://github.com/MartinHjelmare/aiohomeconnect/commit/ff7c1ad8daa700a4a0c50f537ac2f1b690c6999d))
* Remove labels workflow and sync labels ([`09af1f4`](https://github.com/MartinHjelmare/aiohomeconnect/commit/09af1f4050e424bf9df5340154b3eec16b1aa1c1))
* Fix ruff errors ([`c430d13`](https://github.com/MartinHjelmare/aiohomeconnect/commit/c430d1325938799424d5ae70d1bf3b3deade29cf))
* Enable all ruff rules ([`18f9635`](https://github.com/MartinHjelmare/aiohomeconnect/commit/18f9635e842864ee3cce134708aa3540deeb2c52))
* Add pre-commit ([`16f2127`](https://github.com/MartinHjelmare/aiohomeconnect/commit/16f21271ebd474b667fd62166e6fce3a5420c1d3))
* Only support python 3.11+ ([`40a301c`](https://github.com/MartinHjelmare/aiohomeconnect/commit/40a301c887cb0f2eb8f782cc9dcc86b841bb4187))
* Set yaml editor config to indent 2 spaces ([`5fed0cc`](https://github.com/MartinHjelmare/aiohomeconnect/commit/5fed0cce24b9e76e39c98e3baa0784ba0e7864f0))

### Features

* Add base client (#2) ([`9578126`](https://github.com/MartinHjelmare/aiohomeconnect/commit/95781265581a8231b39c76ba9c58f7df606702d5))

### Continuous integration

* Fix labels secret ([`18b65ae`](https://github.com/MartinHjelmare/aiohomeconnect/commit/18b65aec44835c090d7234bd7185fca29b90354b))

## v0.0.0 (2024-01-01)

### Chores

* Create package ([`1b51d7b`](https://github.com/MartinHjelmare/aiohomeconnect/commit/1b51d7ba3e0e00d716e6a1e4a5a6be3e1418ecea))
