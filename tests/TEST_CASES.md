# Petstore API — test cases (working notes)

scope: `POST /pet`, `GET /pet/{id}`, `PUT /pet`  
out of scope (): upload image, store, user

> note: swagger says required in Pet: `name`, `photoUrls`. `status` enum: `available|pending|sold`.  


## core cases

- [ ] **T001** — `POST /pet` — create pet (minimal valid)  
  steps: POST with unique `id`, `name`, `photoUrls=["http://ex.com/p.png"]`  
  expect: `200`; response echoes `id`/`name`; basic Pet shape present

- [ ] **T002** — `GET /pet/{id}` — fetch created pet  
  pre: pet from T001  
  steps: GET by `id`  
  expect: `200`; response `id` matches; has `name`, `photoUrls`, optional `status`

- [ ] **T003** — `PUT /pet` — update existing pet (name + status)  
  pre: pet from T001  
  steps: PUT same `id`, change `name`, `status`→`sold`  
  expect: `200`; response reflects updates

- [ ] **T004** — `GET /pet/{id}` — unknown id  
  steps: GET with large random `id` (e.g., 12-digit)  
  expect: `404` **or** `400` (record what we actually see)

- [ ] **T005** — `POST /pet` — missing required `name`  
  steps: POST without `name`  
  expect: validation error (`400/405`); no pet created

- [ ] **T006** — `POST /pet` — invalid type for `id`  
  steps: POST with `id="abc"`  
  expect: validation error (`400/405`)

- [ ] **T007** — `PUT /pet` — update without `id`  
  steps: PUT body missing `id`  
  expect: `400 "Invalid ID supplied"` or `405 Validation`

- [ ] **T008** — auth header check  
  steps: call POST/GET/PUT without `api_key` header  
  expect: ideally `401/403`; reality: Petstore may ignore header → document actual behavior

---

## additional coverage

- [ ] **T009** — `POST /pet` — parametrize `status ∈ {available,pending,sold}`  
  expect: `200`; response `status` equals posted value

- [ ] **T010** — contract sanity (shape, not strict schema)  
  steps: on T001/T002 responses, assert types for a few fields (`id:int`, `name:str`, `photoUrls:list[str]`)  
  expect: types/keys present; no heavy schema lib

- [ ] **T011** — idempotent-ish update  
  steps: repeat the same `PUT` twice  
  expect: both `200`; second call doesn’t change data further

- [ ] **T012** — cleanup  
  steps: `DELETE /pet/{id}` after tests that create data (best-effort)  
  expect: not strictly asserted; used to keep env tidy


## data + env

- id strategy: `int("9" + 8 random digits)` → avoids collisions w/ small ids
- payload minimal: `{id, name, photoUrls, status?}`
- env:  
