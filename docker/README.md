# Local Postgres bootstrap

The `pg_hba.conf` and `postgresql.conf` in this directory are intended **only**
for a local Postgres container used during development.

- `pg_hba.conf` accepts connections from `0.0.0.0/0` with `scram-sha-256`. This
  is fine inside a development container that is not exposed to the internet,
  but it MUST NOT be reused in production. In production, restrict the CIDR to
  your application's VPC/private subnet.
- `postgresql.conf` sets `listen_addresses = '*'` so the dev container is
  reachable from the host. In production, bind to the internal interface only
  and gate access at the network layer (security group / firewall).

Mount these files into a Postgres container like:

```bash
docker run --name nights-pg \
  -e POSTGRES_PASSWORD=postgres \
  -v "$PWD/docker/pg_hba.conf:/etc/postgresql/pg_hba.conf:ro" \
  -v "$PWD/docker/postgresql.conf:/etc/postgresql/postgresql.conf:ro" \
  -p 5432:5432 \
  postgres:16 -c hba_file=/etc/postgresql/pg_hba.conf -c config_file=/etc/postgresql/postgresql.conf
```
