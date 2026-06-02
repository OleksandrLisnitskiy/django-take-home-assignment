"""Seed sample catalog data for local review and manual testing."""

from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

from catalog.models import Category, Product, Tag


class Command(BaseCommand):
    """Create realistic sample catalog data for reviewer convenience."""

    help = "Seed sample categories, tags, and products for the catalog app."

    # Broad catalog groupings that mirror the business areas a reviewer would
    # expect to see in an electrical supply and contractor procurement system.
    CATEGORY_NAMES = [
        "Electrical Supplies",
        "Construction Tools",
        "Warehouse Materials",
        "Safety Equipment",
        "Contractor Equipment",
        "Inventory and Procurement",
    ]

    # Reusable tags allow the filter UI to demonstrate multi-select behavior.
    TAG_NAMES = [
        "Bulk Order",
        "Commercial Grade",
        "Fast Moving",
        "Indoor Use",
        "Jobsite Ready",
        "Low Voltage",
        "Safety",
        "PPE",
        "Procurement Approved",
        "Weather Resistant",
        "Warehouse Stock",
        "Heavy Duty",
        "Maintenance",
    ]

    PRODUCT_DATA = [
        {
            "name": "12-Gauge Armored Cable Roll",
            "description": (
                "Commercial-grade armored cable for branch circuit installations in "
                "office build-outs, tenant improvements, and warehouse retrofits."
            ),
            "category": "Electrical Supplies",
            "price": Decimal("189.99"),
            "is_active": True,
            "tags": ["Bulk Order", "Commercial Grade", "Low Voltage", "Warehouse Stock"],
        },
        {
            "name": "LED High Bay Fixture",
            "description": (
                "Energy-efficient high bay light fixture designed for distribution "
                "centers, fabrication shops, and large warehouse aisles."
            ),
            "category": "Electrical Supplies",
            "price": Decimal("129.50"),
            "is_active": True,
            "tags": ["Commercial Grade", "Indoor Use", "Fast Moving"],
        },
        {
            "name": "Weatherproof Junction Box Kit",
            "description": (
                "Sealed junction box set for outdoor conduit connections on service "
                "yards, loading docks, and exposed construction zones."
            ),
            "category": "Electrical Supplies",
            "price": Decimal("34.95"),
            "is_active": True,
            "tags": ["Weather Resistant", "Jobsite Ready", "Maintenance"],
        },
        {
            "name": "Cordless Rotary Hammer Drill",
            "description": (
                "Heavy-duty rotary hammer for anchoring conduit racks, mounting "
                "unistrut, and drilling masonry on active construction sites."
            ),
            "category": "Construction Tools",
            "price": Decimal("349.00"),
            "is_active": True,
            "tags": ["Heavy Duty", "Jobsite Ready", "Commercial Grade"],
        },
        {
            "name": "Contractor Circular Saw",
            "description": (
                "Reliable circular saw built for framing crews, plywood breakdown, "
                "and fast turnaround tasks on commercial renovation projects."
            ),
            "category": "Construction Tools",
            "price": Decimal("159.75"),
            "is_active": True,
            "tags": ["Jobsite Ready", "Fast Moving", "Maintenance"],
        },
        {
            "name": "Laser Distance Measure",
            "description": (
                "Compact measuring tool for warehouse planning, shelf spacing, and "
                "field verification during procurement walkthroughs."
            ),
            "category": "Construction Tools",
            "price": Decimal("79.99"),
            "is_active": True,
            "tags": ["Indoor Use", "Procurement Approved", "Fast Moving"],
        },
        {
            "name": "Heavy-Duty Pallet Wrap Bundle",
            "description": (
                "Industrial stretch wrap for outbound shipments, inventory staging, "
                "and securing mixed pallets in warehouse environments."
            ),
            "category": "Warehouse Materials",
            "price": Decimal("58.40"),
            "is_active": True,
            "tags": ["Bulk Order", "Warehouse Stock", "Fast Moving"],
        },
        {
            "name": "Industrial Steel Shelving Bay",
            "description": (
                "Modular shelving bay for parts rooms, MRO inventory, and back-of-house "
                "storage where durable organization matters."
            ),
            "category": "Warehouse Materials",
            "price": Decimal("420.00"),
            "is_active": True,
            "tags": ["Heavy Duty", "Warehouse Stock", "Procurement Approved"],
        },
        {
            "name": "Forklift Safety Barrier Post",
            "description": (
                "Impact-resistant post for separating forklift lanes from pedestrian "
                "zones in busy fulfillment and receiving areas."
            ),
            "category": "Warehouse Materials",
            "price": Decimal("94.25"),
            "is_active": True,
            "tags": ["Warehouse Stock", "Safety", "Heavy Duty", "Commercial Grade"],
        },
        {
            "name": "High-Visibility Safety Vest Pack",
            "description": (
                "ANSI-style reflective vest pack for site visitors, pick teams, and "
                "contractors moving between yard and warehouse operations."
            ),
            "category": "Safety Equipment",
            "price": Decimal("47.80"),
            "is_active": True,
            "tags": ["PPE", "Bulk Order", "Fast Moving"],
        },
        {
            "name": "Cut-Resistant Work Gloves",
            "description": (
                "Grip-enhanced gloves for handling sheet metal, cable reels, and boxed "
                "inventory during receiving and installation work."
            ),
            "category": "Safety Equipment",
            "price": Decimal("18.60"),
            "is_active": True,
            "tags": ["PPE", "Warehouse Stock", "Jobsite Ready"],
        },
        {
            "name": "Hard Hat with Ratchet Suspension",
            "description": (
                "Durable head protection for electricians, warehouse supervisors, and "
                "contractor crews operating around lifts and overhead work."
            ),
            "category": "Safety Equipment",
            "price": Decimal("26.30"),
            "is_active": True,
            "tags": ["PPE", "Commercial Grade", "Jobsite Ready"],
        },
        {
            "name": "Portable Jobsite Generator",
            "description": (
                "Gas-powered generator that supports temporary lighting, portable tools, "
                "and service trailers on sites without permanent power."
            ),
            "category": "Contractor Equipment",
            "price": Decimal("899.00"),
            "is_active": True,
            "tags": ["Heavy Duty", "Jobsite Ready", "Weather Resistant"],
        },
        {
            "name": "Mobile Material Lift",
            "description": (
                "Compact lifting equipment for raising duct, conduit bundles, and "
                "mechanical components during interior fit-out work."
            ),
            "category": "Contractor Equipment",
            "price": Decimal("1249.99"),
            "is_active": True,
            "tags": ["Commercial Grade", "Heavy Duty", "Maintenance"],
        },
        {
            "name": "All-Terrain Extension Ladder",
            "description": (
                "Rugged extension ladder suited to uneven surfaces, exterior service "
                "calls, and fast access around contractor staging areas."
            ),
            "category": "Contractor Equipment",
            "price": Decimal("215.50"),
            "is_active": True,
            "tags": ["Weather Resistant", "Jobsite Ready", "Commercial Grade"],
        },
        {
            "name": "Barcode Inventory Scanner",
            "description": (
                "Handheld scanner for stock counts, bin transfers, and purchase order "
                "receiving in warehouse and procurement workflows."
            ),
            "category": "Inventory and Procurement",
            "price": Decimal("299.00"),
            "is_active": True,
            "tags": ["Warehouse Stock", "Procurement Approved", "Fast Moving"],
        },
        {
            "name": "Procurement Clipboards Pack",
            "description": (
                "Weather-resistant clipboards for purchase verification, field audits, "
                "and inventory recounts across yard and warehouse teams."
            ),
            "category": "Inventory and Procurement",
            "price": Decimal("21.45"),
            "is_active": True,
            "tags": ["Bulk Order", "Procurement Approved", "Weather Resistant"],
        },
        {
            "name": "Thermal Label Printer",
            "description": (
                "Desktop label printer for asset tags, pallet labels, and receiving "
                "identification in fast-moving inventory operations."
            ),
            "category": "Inventory and Procurement",
            "price": Decimal("245.00"),
            "is_active": True,
            "tags": ["Warehouse Stock", "Procurement Approved", "Indoor Use"],
        },
        {
            "name": "Rechargeable Work Light",
            "description": (
                "Portable work light for service calls, dim warehouse corners, and "
                "temporary inspection stations during maintenance rounds."
            ),
            "category": "Electrical Supplies",
            "price": Decimal("64.99"),
            "is_active": True,
            "tags": ["Maintenance", "Indoor Use", "Jobsite Ready"],
        },
        {
            "name": "Diamond Cutoff Blade",
            "description": (
                "High-performance blade for concrete and masonry cutting on renovation "
                "jobs that require precise, durable tool accessories."
            ),
            "category": "Construction Tools",
            "price": Decimal("48.20"),
            "is_active": True,
            "tags": ["Heavy Duty", "Jobsite Ready", "Fast Moving"],
        },
        {
            "name": "Spill Control Absorbent Pads",
            "description": (
                "Quick-response absorbent pads for oil, chemical, and liquid cleanup in "
                "maintenance bays, loading docks, and warehouse aisles."
            ),
            "category": "Warehouse Materials",
            "price": Decimal("39.90"),
            "is_active": True,
            "tags": ["Safety", "Warehouse Stock", "Maintenance"],
        },
        {
            "name": "Face Shield Assembly",
            "description": (
                "Clear face shield with adjustable headgear for grinding, cutting, and "
                "splash protection in industrial service environments."
            ),
            "category": "Safety Equipment",
            "price": Decimal("31.15"),
            "is_active": True,
            "tags": ["PPE", "Commercial Grade", "Maintenance"],
        },
    ]

    @transaction.atomic
    def handle(self, *args, **options):
        """Seed categories, tags, and products in a single database transaction."""
        categories = self._create_categories()
        tags = self._create_tags()
        product_count = self._create_products(categories=categories, tags=tags)

        self.stdout.write(
            self.style.SUCCESS(
                "Seeded sample catalog data: "
                f"{len(categories)} categories, {len(tags)} tags, {product_count} products."
            )
        )

    def _create_categories(self):
        """Create or update categories and return them keyed by display name."""
        categories = {}
        for name in self.CATEGORY_NAMES:
            category, _ = Category.objects.update_or_create(
                slug=slugify(name),
                defaults={"name": name},
            )
            categories[name] = category
        return categories

    def _create_tags(self):
        """Create or update tags and return them keyed by display name."""
        tags = {}
        for name in self.TAG_NAMES:
            tag, _ = Tag.objects.update_or_create(
                slug=slugify(name),
                defaults={"name": name},
            )
            tags[name] = tag
        return tags

    def _create_products(self, categories, tags):
        """Create or update products and assign their many-to-many tag relations."""
        for product_data in self.PRODUCT_DATA:
            # Product names act as the stable identifier so the seed command can be
            # run repeatedly without creating duplicate records.
            product, _ = Product.objects.update_or_create(
                name=product_data["name"],
                defaults={
                    "description": product_data["description"],
                    "category": categories[product_data["category"]],
                    "price": product_data["price"],
                    "is_active": product_data["is_active"],
                },
            )
            # Reset the tag mapping on every run so data stays consistent if the
            # sample definitions change over time.
            product.tags.set([tags[tag_name] for tag_name in product_data["tags"]])

        return len(self.PRODUCT_DATA)
