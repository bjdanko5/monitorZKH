-- Update the sequence to the maximum id + 1 from the mzkh_roles table
DO $$
DECLARE
    max_id BIGINT;
BEGIN
    -- Get the maximum id from the mzkh_roles table
    SELECT COALESCE(MAX(id), 0) INTO max_id FROM mzkh_edizms;

    -- Set the sequence to max_id + 1
    PERFORM setval('mzkh_edizms_id_seq', max_id + 1);
END $$;

"public","mzkh_edizms_id_seq"
"public","mzkh_roles_id_seq"
"public","mzkh_orgs_id_seq"
"public","mzkh_files_id_seq"
"public","mzkh_options_id_seq"
"public","mzkh_datum_types_id_seq"
"public","mzkh_subsystems_id_seq"
"public","mzkh_users_id_seq"
"public","mzkh_datums_id_seq"
"public","mzkh_datum_values_id_seq"




DO $$
DECLARE
    seq_record RECORD;
    max_id BIGINT;
BEGIN
    -- Loop through each sequence in the public schema
    FOR seq_record IN
        SELECT sequence_name
        FROM information_schema.sequences
        WHERE sequence_schema = 'public'
    LOOP
        -- Construct the dynamic SQL to get the maximum id for the corresponding table
        EXECUTE format('SELECT COALESCE(MAX(id), 0) FROM %I', replace(seq_record.sequence_name, '_id_seq', ''))
        INTO max_id;

        -- Set the sequence to max_id + 1
        EXECUTE format('SELECT setval(%L, %s + 1)', seq_record.sequence_name, max_id);
    END LOOP;
END $$;