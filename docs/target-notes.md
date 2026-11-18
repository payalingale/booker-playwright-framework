# Target notes: Restful Booker Platform (automationintesting.online)

## App

- Guest can: browse rooms, book a room for dates, send a contact message
- Admin can: log in, create/edit/delete rooms, view and manage bookings, read messages, edit branding

## Auth

- Login: POST /api/auth/login body: {"username": "...", "password": "..."}
- Response body: {"token": "<value>"}
- Protected calls (e.g. POST /api/room) read a COOKIE named `token`
- → Auth is a cookie. The API client sends `Cookie: token=<value>`;
  the browser context gets the same cookie → one login serves both layers

## API endpoints (from the app's route files)

| Method         | URL                | What                                   |
| -------------- | ------------------ | -------------------------------------- |
| POST           | /api/auth/login    | admin login → token                    |
| POST           | /api/auth/validate | check a token                          |
| GET/POST       | /api/room          | list / create rooms (POST needs token) |
| GET/PUT/DELETE | /api/room/{id}     | one room                               |
| GET/POST       | /api/booking       | list / create bookings                 |
| GET/PUT/DELETE | /api/booking/{id}  | one booking                            |
| GET/POST       | /api/message       | contact messages                       |
| GET            | /api/report        | booking calendar report                |

## Decisions

- Can create/delete rooms: yes (admin, with token cookie) → tests can own their room data
- Smoke flows:
  1. Admin login via API returns a token
  2. Admin creates a room via API → it appears on the public site
  3. Guest books an available room → booking confirmed
