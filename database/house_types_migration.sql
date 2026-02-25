-- Migration: Create house_types table
-- Date: 2026-02-15
-- Purpose: Store house type catalog information for admin management

CREATE TABLE IF NOT EXISTS house_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price_start DECIMAL(15, 2),
    type_category VARCHAR(50) DEFAULT 'Modern',
    land_size VARCHAR(50),
    building_size VARCHAR(50),
    bedrooms INT DEFAULT 0,
    bathrooms INT DEFAULT 0,
    floors INT DEFAULT 1,
    carport INT DEFAULT 0,
    image_url TEXT,
    features JSON,
    specifications JSON,
    is_active TINYINT(1) DEFAULT 1,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (type_category),
    INDEX idx_active (is_active),
    INDEX idx_order (display_order)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default house types from current HouseTypes.js page
INSERT INTO house_types (name, description, price_start, type_category, land_size, building_size, bedrooms, bathrooms, floors, carport, image_url, features, specifications, display_order) VALUES
(
    'Rumah Modern',
    'Desain kontemporer dengan sentuhan modern. Cocok untuk keluarga muda yang menginginkan gaya hidup praktis dan elegan.',
    850000000,
    'Modern',
    '10x15 m',
    '120 m²',
    3,
    2,
    2,
    1,
    '/assets/house-modern.jpg',
    JSON_ARRAY('Smart Home Ready', 'Open Space Concept', 'Large Windows', 'Modern Kitchen', 'Private Garden'),
    JSON_OBJECT('Luas Tanah', '10x15 m', 'Luas Bangunan', '120 m²', 'Kamar Tidur', '3', 'Kamar Mandi', '2', 'Lantai', '2', 'Carport', '1'),
    1
),
(
    'Rumah Klasik',
    'Arsitektur klasik yang timeless dengan detail ornamen yang elegan. Memberikan kesan mewah dan berkelas.',
    1200000000,
    'Classic',
    '12x20 m',
    '180 m²',
    4,
    3,
    2,
    2,
    '/assets/house-classic.jpg',
    JSON_ARRAY('Classic Architecture', 'Elegant Details', 'Spacious Rooms', 'Grand Entrance', 'Luxury Finishes'),
    JSON_OBJECT('Luas Tanah', '12x20 m', 'Luas Bangunan', '180 m²', 'Kamar Tidur', '4', 'Kamar Mandi', '3', 'Lantai', '2', 'Carport', '2'),
    2
),
(
    'Rumah Contemporary',
    'Perpaduan unik antara modern dan minimalis. Desain inovatif dengan material berkualitas tinggi.',
    950000000,
    'Contemporary',
    '10x18 m',
    '140 m²',
    3,
    2,
    2,
    1,
    '/assets/house-contemporary.jpg',
    JSON_ARRAY('Unique Design', 'High Ceiling', 'Natural Lighting', 'Premium Materials', 'Eco-Friendly'),
    JSON_OBJECT('Luas Tanah', '10x18 m', 'Luas Bangunan', '140 m²', 'Kamar Tidur', '3', 'Kamar Mandi', '2', 'Lantai', '2', 'Carport', '1'),
    3
),
(
    'Rumah Industrial',
    'Gaya industrial yang trendy dengan ekspos material. Perfect untuk yang suka tampilan bold dan edgy.',
    780000000,
    'Industrial',
    '9x15 m',
    '110 m²',
    3,
    2,
    1,
    1,
    '/assets/house-industrial.jpg',
    JSON_ARRAY('Exposed Brick', 'Metal Accents', 'Open Layout', 'Loft Style', 'Urban Design'),
    JSON_OBJECT('Luas Tanah', '9x15 m', 'Luas Bangunan', '110 m²', 'Kamar Tidur', '3', 'Kamar Mandi', '2', 'Lantai', '1', 'Carport', '1'),
    4
);

-- Add sample data indicator
SELECT 'house_types table created and populated with 4 default house types' AS status;
