# Changelog

## v0.16.1 (2025-03-04)

## v0.16.0 (2025-03-01)

### Features

* Improve exceptions and cli logging (#61) ([`62b1bbc`](https://github.com/MartinHjelmare/aiohomeconnect/commit/62b1bbce54236fcba758bb0c3d8a9baec7b2c0e2))

## v0.15.1 (2025-02-27)

### Bug fixes

* Missing error handling at get available commands endpoint (#60) ([`2bf902b`](https://github.com/MartinHjelmare/aiohomeconnect/commit/2bf902b795e5987eed2b758e3ed363b3e0fbbd7f))

## v0.15.0 (2025-02-25)

### Features

* Add retry after info from rate limit error (#58) ([`675aa3f`](https://github.com/MartinHjelmare/aiohomeconnect/commit/675aa3f8b85feb0ea1975460b45d65f53f985962))

## v0.14.0 (2025-02-25)

### Features

* Add cavity temperature (#59) ([`a160e37`](https://github.com/MartinHjelmare/aiohomeconnect/commit/a160e37167038cb38b4174f210841f3ae0f9e622))

## v0.13.0 (2025-02-20)

### Features

* Add set selected program option to cli (#57) ([`29a68cf`](https://github.com/MartinHjelmare/aiohomeconnect/commit/29a68cf686de140bd34226191f8554ea1b162946))

### Build system

* Run copier update (#54) ([`712d2b4`](https://github.com/MartinHjelmare/aiohomeconnect/commit/712d2b45765b6f91147164c8292b96a22b500a4d))

## v0.12.3 (2025-02-01)

### Bug fixes

* Make program model key optional (#53) ([`9d354ec`](https://github.com/MartinHjelmare/aiohomeconnect/commit/9d354ec82996fae80cec1d5d9d69b712b73af80d))

## v0.12.2 (2025-01-31)

### Bug fixes

* Include debug log of request and response and sse event (#52) ([`9e0a719`](https://github.com/MartinHjelmare/aiohomeconnect/commit/9e0a71921b5aca2909ac406190117c0c7aa8640b))

## v0.12.1 (2025-01-29)

### Bug fixes

* Use `raw_key` for the correct dataclasses for programs (#51) ([`a489f6e`](https://github.com/MartinHjelmare/aiohomeconnect/commit/a489f6eaaeeed7b0da8e9f6a8f5d676cbcb899d4))

## v0.12.0 (2025-01-29)

### Features

* Add `raw_key` field (#50) ([`d7ed726`](https://github.com/MartinHjelmare/aiohomeconnect/commit/d7ed72636a2af53f3a7ced3f6f477e5e20d27ba0))

## v0.11.4 (2025-01-25)

### Bug fixes

* Ignore `none` values at models used at `put` requests (#48) ([`6d8000f`](https://github.com/MartinHjelmare/aiohomeconnect/commit/6d8000f99044a704274394cb097232943609d165))

## v0.11.3 (2025-01-24)

### Bug fixes

* Update dependency fastapi to v0.115.7 ([`9979e6d`](https://github.com/MartinHjelmare/aiohomeconnect/commit/9979e6dddcd49da9870e9a746d2a298d5bc36349))

## v0.11.2 (2025-01-17)

### Bug fixes

* Fix requests that have a body (#46) ([`13134f4`](https://github.com/MartinHjelmare/aiohomeconnect/commit/13134f4bb3d5e6409120958ef79d2e6e579af52d))

## v0.11.1 (2025-01-16)

### Bug fixes

* Raise exception only on error request (#45) ([`e5479a7`](https://github.com/MartinHjelmare/aiohomeconnect/commit/e5479a7577d208a0ed6863a083f6e689eb875b96))

## v0.11.0 (2025-01-14)

### Features

* Reference options, settings, and status enum keys at events enum (#43) ([`e391340`](https://github.com/MartinHjelmare/aiohomeconnect/commit/e391340c3af2c3545f5d6f404784e9e0a3ba7d1a))

## v0.10.0 (2025-01-13)

### Features

* Raise exceptions on http errors (#44) ([`112cd75`](https://github.com/MartinHjelmare/aiohomeconnect/commit/112cd75094285117201d0672072ec61d0ffcd7a5))

## v0.9.0 (2025-01-10)

### Features

* Support unknown enum values (#41) ([`efced94`](https://github.com/MartinHjelmare/aiohomeconnect/commit/efced94961f56e1f6621c587113f18d067231158))

## v0.8.0 (2025-01-09)

### Features

* Complete string enumerations and fix names (#40) ([`b92e281`](https://github.com/MartinHjelmare/aiohomeconnect/commit/b92e2818623a4d72539eb362cbe5721d14d43e31))

## v0.7.5 (2025-01-06)

### Bug fixes

* Set default values for optional model attributes (#37) ([`bb2744a`](https://github.com/MartinHjelmare/aiohomeconnect/commit/bb2744a165fbcab5e0de9a4c58e10e7d5f6a0a66))

## v0.7.4 (2025-01-06)

### Bug fixes

* Home appliance model (#36) ([`5cd6e06`](https://github.com/MartinHjelmare/aiohomeconnect/commit/5cd6e064673bff8df9c9fc5ec4f8259682d2b58e))

## v0.7.3 (2024-12-20)

### Bug fixes

* Update dependency authlib to v1.4.0 ([`be1d018`](https://github.com/MartinHjelmare/aiohomeconnect/commit/be1d018b1b21d10ef91d438ec65663da7bad9447))

## v0.7.2 (2024-12-15)

### Bug fixes

* Update dependency uvicorn to ^0.34.0 ([`a36533c`](https://github.com/MartinHjelmare/aiohomeconnect/commit/a36533c29baa1786c98e8d00cb145ad4be1c131f))

## v0.7.1 (2024-12-14)

### Bug fixes

* Update dependency uvicorn to ^0.33.0 ([`0f91cc5`](https://github.com/MartinHjelmare/aiohomeconnect/commit/0f91cc5f8c37027469fd7b0ded6e35489a825698))

## v0.7.0 (2024-12-12)

### Features

* Add sse streams (#34) ([`36a53a4`](https://github.com/MartinHjelmare/aiohomeconnect/commit/36a53a4eedac701b359857f1f75475fcec5547c3))

## v0.6.4 (2024-12-07)

### Bug fixes

* Update dependency httpx to v0.28.1 ([`8939e1c`](https://github.com/MartinHjelmare/aiohomeconnect/commit/8939e1c7324683a520c79b2f34227875825bd697))

## v0.6.3 (2024-12-04)

### Bug fixes

* Update dependency typer to v0.15.1 ([`5fd604d`](https://github.com/MartinHjelmare/aiohomeconnect/commit/5fd604d740bea69d2c7166033795471ac6507b2d))

## v0.6.2 (2024-12-04)

### Bug fixes

* Update dependency fastapi to v0.115.6 ([`984e2eb`](https://github.com/MartinHjelmare/aiohomeconnect/commit/984e2ebc10baee0fef5189b9b5b8c9d7ff61eb8f))

## v0.6.1 (2024-12-03)

### Bug fixes

* Update dependency typer to ^0.15.0 ([`ff03685`](https://github.com/MartinHjelmare/aiohomeconnect/commit/ff03685e24742ee80cfd085b761bd0d5102d2beb))

## v0.6.0 (2024-11-30)

### Features

* Add dishwasher keys (#31) ([`496079f`](https://github.com/MartinHjelmare/aiohomeconnect/commit/496079fa4cc6a5e7e6d207710cc24d9a94e6c960))

## v0.5.2 (2024-11-29)

### Bug fixes

* Update httpx ([`a3cc541`](https://github.com/MartinHjelmare/aiohomeconnect/commit/a3cc541b5e1bbfad93f72c7d1633d0d05c908c32))

## v0.5.1 (2024-11-29)

### Bug fixes

* Update dependency typer to ^0.14.0 ([`f1fd272`](https://github.com/MartinHjelmare/aiohomeconnect/commit/f1fd272aceab684fd1bdee711077108cbcc0df3f))

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

## v0.2.12 (2024-11-21)

### Bug fixes

* Update dependency uvicorn to v0.32.1 ([`d9b8b88`](https://github.com/MartinHjelmare/aiohomeconnect/commit/d9b8b881ad309d7a5f622d5741fab340930d11a4))

## v0.2.11 (2024-11-19)

### Bug fixes

* Update dependency typer to v0.13.1 ([`1c96fba`](https://github.com/MartinHjelmare/aiohomeconnect/commit/1c96fbad25a86f3381d00a619ddb655a31d72ed1))

## v0.2.10 (2024-11-12)

### Bug fixes

* Update dependency fastapi to v0.115.5 ([`c07099b`](https://github.com/MartinHjelmare/aiohomeconnect/commit/c07099b8797116ec6987fe1e5d97c8114018c7ba))

## v0.2.9 (2024-11-08)

### Bug fixes

* Update dependency typer to ^0.13.0 ([`b450fda`](https://github.com/MartinHjelmare/aiohomeconnect/commit/b450fda42a96b21c39b31e45798e04f822686d12))

## v0.2.8 (2024-11-01)

### Bug fixes

* Update dependency rich to v13.9.4 ([`60bc03b`](https://github.com/MartinHjelmare/aiohomeconnect/commit/60bc03b271a53df28fd37145f64846ea3d97640b))

## v0.2.7 (2024-10-28)

### Bug fixes

* Update dependency fastapi to v0.115.4 ([`6e546d9`](https://github.com/MartinHjelmare/aiohomeconnect/commit/6e546d9be4aa24c51d01194452f1121ed7f414a3))

## v0.2.6 (2024-10-24)

### Bug fixes

* Update dependency mashumaro to v3.14 ([`0ee6d7f`](https://github.com/MartinHjelmare/aiohomeconnect/commit/0ee6d7fe3e25ce6896b0783d03ef780aa82a555e))

## v0.2.5 (2024-10-22)

### Bug fixes

* Update dependency rich to v13.9.3 ([`8bb77ee`](https://github.com/MartinHjelmare/aiohomeconnect/commit/8bb77ee3893eb6f1c7d246fbda161ac032dae762))

## v0.2.4 (2024-10-22)

### Bug fixes

* Update dependency fastapi to v0.115.3 ([`f6a6283`](https://github.com/MartinHjelmare/aiohomeconnect/commit/f6a6283b22582e2e0e4556f032415b132f2a1794))

## v0.2.3 (2024-10-15)

### Bug fixes

* Update dependency uvicorn to ^0.32.0 ([`49d3f81`](https://github.com/MartinHjelmare/aiohomeconnect/commit/49d3f81b3e0e488105f7a7f5b8af9307b04311bf))

## v0.2.2 (2024-10-12)

### Bug fixes

* Update dependency fastapi to v0.115.2 ([`ccb61a0`](https://github.com/MartinHjelmare/aiohomeconnect/commit/ccb61a0a0a2afbcf27d75bb0ba8f6d7ef4f743c5))

## v0.2.1 (2024-10-10)

### Bug fixes

* Update dependency uvicorn to v0.31.1 ([`285c771`](https://github.com/MartinHjelmare/aiohomeconnect/commit/285c771dbc0c76f47a01dfd05c64b435a293ef1c))

## v0.2.0 (2024-10-07)

### Features

* Add swagger parser (#12) ([`aefbefa`](https://github.com/MartinHjelmare/aiohomeconnect/commit/aefbefa9378c7a505e1fca93c28dce69a3a9a46f))

## v0.1.9 (2024-10-04)

### Bug fixes

* Update dependency rich to v13.9.2 ([`7513478`](https://github.com/MartinHjelmare/aiohomeconnect/commit/751347844d7e32996b6b8ffb7651502fd28f1144))

## v0.1.8 (2024-10-01)

### Bug fixes

* Update dependency rich to v13.9.1 ([`7737f85`](https://github.com/MartinHjelmare/aiohomeconnect/commit/7737f85453212005bb9c55bffdd5a7d131763a7c))

## v0.1.7 (2024-09-28)

### Bug fixes

* Update dependency uvicorn to ^0.31.0 ([`d42aafd`](https://github.com/MartinHjelmare/aiohomeconnect/commit/d42aafdbee1c96658f520cec0a05a2a013750ce7))

## v0.1.6 (2024-09-18)

### Bug fixes

* Update dependency fastapi to ^0.115.0 ([`ddfa69a`](https://github.com/MartinHjelmare/aiohomeconnect/commit/ddfa69a4a03ad2639815dc341637d88cea82d44a))

## v0.1.5 (2024-09-14)

### Bug fixes

* Update dependency fastapi to v0.114.2 ([`d6696fc`](https://github.com/MartinHjelmare/aiohomeconnect/commit/d6696fc00c89a6948349f4102e5066242be8b3ab))

## v0.1.4 (2024-09-11)

### Bug fixes

* Update dependency fastapi to v0.114.1 ([`aef28b9`](https://github.com/MartinHjelmare/aiohomeconnect/commit/aef28b92e7ab2db460f9e181cee441c139429112))

## v0.1.3 (2024-09-10)

### Bug fixes

* Update dependency rich to v13.8.1 ([`6a8e428`](https://github.com/MartinHjelmare/aiohomeconnect/commit/6a8e4288887871d8c7ad844b08f5fc13d273b079))

## v0.1.2 (2024-09-07)

### Bug fixes

* Update dependency fastapi to ^0.114.0 ([`867393c`](https://github.com/MartinHjelmare/aiohomeconnect/commit/867393c0f36fcc581e487616f1d510118ff415a7))

## v0.1.1 (2024-08-29)

### Bug fixes

* Update dependency typer to ^0.12.0 ([`b3f841d`](https://github.com/MartinHjelmare/aiohomeconnect/commit/b3f841dabb1e6072d120b78219d16e8f8ae7a827))

## v0.1.0 (2024-08-28)

### Features

* Add base client (#2) ([`9578126`](https://github.com/MartinHjelmare/aiohomeconnect/commit/95781265581a8231b39c76ba9c58f7df606702d5))

## v0.0.0 (2024-01-01)
