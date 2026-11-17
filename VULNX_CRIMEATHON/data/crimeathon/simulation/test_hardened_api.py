from mock_api_server import create_app


def run_checks():
    client = create_app("hardened").test_client()

    attendance = client.get("/attendance", headers={"Authorization": "Bearer attendance"})
    assert attendance.status_code == 200, attendance.get_data(as_text=True)

    denied_search = client.get("/learner/search", headers={"Authorization": "Bearer attendance"})
    assert denied_search.status_code == 403, denied_search.get_data(as_text=True)

    denied_export = client.get("/learner/export", headers={"Authorization": "Bearer attendance"})
    assert denied_export.status_code == 403, denied_export.get_data(as_text=True)

    denied_source = client.get(
        "/learner/search",
        headers={"Authorization": "Bearer attendance", "X-Source": "external"},
    )
    assert denied_source.status_code == 403, denied_source.get_data(as_text=True)

    invalid_auth = client.get("/learner/search", headers={"Authorization": "Bearer unknown"})
    assert invalid_auth.status_code == 401, invalid_auth.get_data(as_text=True)

    print("All five hardened-mode checks passed.")


if __name__ == "__main__":
    run_checks()
