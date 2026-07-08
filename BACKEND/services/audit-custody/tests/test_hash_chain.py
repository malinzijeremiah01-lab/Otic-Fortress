from audit_custody.hash_chain import hash_record

def test_hash_record():
    assert len(hash_record({"a": 1})) == 64
