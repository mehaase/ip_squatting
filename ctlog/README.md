Candidate domain names are read from Certificate Transparency logs. This means,
of course, that only domains which have ceritficates issued by public
authorities will be discovered. A public search engine at https://crt.sh/
records CT log data into a relational database. The records can be queried on
their website or by connecting directly to their Postgres server.

Connect to Postgres:

    $ psql -h crt.sh -p 5432 -U guest certwatch

You can use the web interface and append `&showSQL=y` to any search query in
order to display the SQL used. Here's an example:

    SELECT ci.ISSUER_CA_ID,
            ca.NAME ISSUER_NAME,
            ci.NAME_VALUE NAME_VALUE,
            min(c.ID) MIN_CERT_ID,
            min(ctle.ENTRY_TIMESTAMP) MIN_ENTRY_TIMESTAMP,
            x509_notBefore(c.CERTIFICATE) NOT_BEFORE,
            x509_notAfter(c.CERTIFICATE) NOT_AFTER
        FROM ca,
            ct_log_entry ctle,
            certificate_identity ci,
            certificate c
        WHERE ci.ISSUER_CA_ID = ca.ID
            AND c.ID = ctle.CERTIFICATE_ID
            AND reverse(lower(ci.NAME_VALUE)) LIKE reverse('%markhaa.se')
            AND ci.CERTIFICATE_ID = c.ID
        GROUP BY c.ID, ci.ISSUER_CA_ID, ISSUER_NAME, NAME_VALUE
        ORDER BY MIN_ENTRY_TIMESTAMP DESC, NAME_VALUE, ISSUER_NAME;

Notice that searching for a wildcard prefix can be accomplished with two
`reverse()` calls. Searching for a wildcard prefix directly will timeout the
query.
