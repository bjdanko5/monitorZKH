select
    namespace.NAME,
    namespace.TYPENAME,
    ADMHIERARCHY.REGIONCODE
FROM
    ADMHIERARCHY
    join namespace on ADMHIERARCHY.OBJECTID = namespace.OBJECTID
where
    ADMHIERARCHY.Level = 0
order by
    ADMHIERARCHY.REGIONCODE