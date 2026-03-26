"""
Management command to populate sample data
Usage: python manage.py populate_sample_data
"""
from django.core.management.base import BaseCommand
from products.models import Product
from django.utils import timezone


class Command(BaseCommand):
    help = 'Populate the database with sample products'

    def handle(self, *args, **options):
        # Check if products already exist
        if Product.objects.exists():
            self.stdout.write(
                self.style.WARNING('Products already exist in database. Skipping...')
            )
            return

        # Sample electrical products
        sample_products = [
            {
                'name': 'LED Bulb - 15W',
                'model': 'LED-2024-15W',
                'description': 'High-brightness LED light bulb, 15W, 1200 lumens, cool white (6500K), '
                             'energy efficient, long lifespan of 20,000+ hours. Perfect for homes and offices.'
            },
            {
                'name': 'Power Supply Unit',
                'model': 'PSU-2024-500W',
                'description': 'Industrial grade power supply, 500W capacity, AC to DC conversion, '
                             'regulated output voltage, wide input range (85-265V). Ideal for heavy machinery and equipment.'
            },
            {
                'name': 'Electric Motor - 1.5 HP',
                'model': 'MOT-2024-1.5HP',
                'description': '3-phase electric motor, 1.5 horsepower, 1400 RPM, high efficiency rating, '
                             'compact design, suitable for pumps and compressors.'
            },
            {
                'name': 'Transformer - 100VA',
                'model': 'TRANS-2024-100VA',
                'description': 'Step-down transformer, 100VA capacity, converts 220V to 12V AC, '
                             'overheat protection, reliable for light applications.'
            },
            {
                'name': 'Relay Module - 8 Channel',
                'model': 'RELAY-2024-8CH',
                'description': '8-channel relay module for automation, 24VDC coil voltage, '
                             'high current capacity per channel, compact DIN rail mount.'
            },
            {
                'name': 'Circuit Breaker - 32A',
                'model': 'CB-2024-32A',
                'description': '32A single-pole circuit breaker, thermal and magnetic protection, '
                             'Din rail mount, meets IEC standards, suitable for residential circuits.'
            },
            {
                'name': 'Contactor - 40A',
                'model': 'CONT-2024-40A',
                'description': '3-phase contactor, 40A rating, AC coil 220V, robust design, '
                             'widely used in industrial automation applications.'
            },
            {
                'name': 'Junction Box - Plastic',
                'model': 'JB-2024-PLASTIC',
                'description': 'IP65 rated plastic junction box, weatherproof, cable gland provision, '
                             'suitable for both indoor and outdoor installations.'
            },
            {
                'name': 'Cable Crimper Tool',
                'model': 'TOOL-2024-CRIMP',
                'description': 'Heavy-duty cable crimper for wire terminals, adjustable for different sizes, '
                             'professional grade tool for electricians.'
            },
            {
                'name': 'Voltmeter - Digital',
                'model': 'VOLT-2024-DIG',
                'description': 'Digital voltmeter, measures DC 0-1000V, AC 0-750V, accuracy ±1.5%, '
                             'with LCD display for easy reading.'
            },
        ]

        # Create products
        for product_data in sample_products:
            product, created = Product.objects.get_or_create(
                model=product_data['model'],
                defaults={
                    'name': product_data['name'],
                    'description': product_data['description'],
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✓ Created product: {product.name} ({product.model})'
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f'- Product already exists: {product.name}'
                    )
                )

        self.stdout.write(
            self.style.SUCCESS('✓ Sample data population complete!')
        )
