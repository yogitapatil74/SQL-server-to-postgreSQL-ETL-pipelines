DO $body$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$role') THEN
        CREATE ROLE $role WITH LOGIN PASSWORD '$password';
    ELSE
        ALTER ROLE $role WITH LOGIN PASSWORD '$password';
    END IF;
END
$body$;
