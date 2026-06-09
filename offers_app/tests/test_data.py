"""
Test Data Fixtures for the Offers Application Test Suite.

This module houses the standardized data structures representing valid payload
structures sent during creation and update operations in integration tests.
"""

VALID_OFFER_POST_DATA = {
    "title": "Grafikdesign-Paket",
    "image": None,
    "description": "Ein umfassendes Grafikdesign-Paket für Unternehmen.",
    "details": [
        {
            "title": "Basic Design",
            "revisions": 2,
            "delivery_time_in_days": 5,
            "price": 100,
            "features":
            ["Logo Design", "Visitenkarte"],
            "offer_type": "basic"
        },
        {
            "title": "Standard Design",
            "revisions": 5,
            "delivery_time_in_days": 7,
            "price": 200,
            "features":
            ["Logo Design", "Visitenkarte", "Briefpapier"],
            "offer_type": "standard"
        },
        {
            "title": "Premium Design",
            "revisions": 10,
            "delivery_time_in_days": 10,
            "price": 500,
            "features":
            ["Logo Design", "Visitenkarte", "Briefpapier", "Flyer"],
            "offer_type": "premium"
        }
    ]
}
"""
dict: Valid payload object for simulating an Offer creation workflow
(POST request), including nested configurations for all three package
pricing tiers.
"""

VALID_OFFER_PATCH_DATA = {
    "title": "Updated Grafikdesign-Paket",
    "details": [
        {
            "title": "Basic Design Updated",
            "revisions": 3,
            "delivery_time_in_days": 6,
            "price": 120,
            "features": ["Logo Design", "Flyer"],
            "offer_type": "basic"
        }
    ]
}
"""
dict: Valid payload object for partial modification updates (PATCH request),
targeting target values within the top-level entity properties and modifying
specific nested child details.
"""
