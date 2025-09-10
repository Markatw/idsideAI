// Basic constraints for unique ids
CREATE CONSTRAINT node_id_unique IF NOT EXISTS FOR (n) REQUIRE n.id IS UNIQUE;
CREATE INDEX by_tenant IF NOT EXISTS FOR (n) ON (n.tenant_id, n.workspace_id);

// Labels (optional examples)
CREATE INDEX decision_title IF NOT EXISTS FOR (d:Decision) ON (d.title);
CREATE INDEX evidence_created IF NOT EXISTS FOR (e:Evidence) ON (e.created_at);

// Sample seed
MERGE (d:Decision {id:'DEC-1', title:'Decision: Select Supplier'});
MERGE (a:Option {id:'OPT-A', title:'Option A — Vendor Alpha'});
MERGE (b:Option {id:'OPT-B', title:'Option B — Vendor Beta'});
MERGE (e:Evidence {id:'EV-42', title:'ISO 27001'});
MERGE (r:Risk {id:'RSK-1', title:'Risk: Vendor Lock‑in'});
MERGE (d)-[:CONSIDERS]->(a);
MERGE (d)-[:CONSIDERS]->(b);
MERGE (e)-[:SUPPORTED_BY]->(a);
MERGE (b)-[:INCURS]->(r);
