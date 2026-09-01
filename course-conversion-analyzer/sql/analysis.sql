-- 1. Average conversion rate
SELECT
    ROUND(AVG(conversion_rate), 4) AS average_conversion
FROM courses;

-- 2. Top 3 most-viewed courses
SELECT
    course_id,
    course_name,
    views,
    enrollments,
    conversion_rate
FROM courses
ORDER BY views DESC
LIMIT 3;

-- 3. Bottom 3 conversion rates
SELECT
    course_id,
    course_name,
    views,
    enrollments,
    conversion_rate
FROM courses
ORDER BY conversion_rate ASC
LIMIT 3;

-- 4. High-view / low-conversion courses
SELECT
    course_id,
    course_name,
    category,
    price,
    rating,
    views,
    preview_clicks,
    enrollments,
    ROUND(conversion_rate, 4) AS conversion_rate
FROM courses
WHERE high_view_low_conversion = 1;

-- 5. Conversion by category
SELECT
    category,
    COUNT(*) AS number_of_courses,
    ROUND(AVG(views), 2) AS average_views,
    ROUND(AVG(conversion_rate), 4) AS average_conversion
FROM courses
GROUP BY category
ORDER BY average_conversion DESC;

-- 6. Problematic courses vs other courses
SELECT
    high_view_low_conversion,
    COUNT(*) AS number_of_courses,
    ROUND(AVG(price), 2) AS average_price,
    ROUND(AVG(rating), 2) AS average_rating,
    ROUND(AVG(conversion_rate), 4) AS average_conversion
FROM courses
GROUP BY high_view_low_conversion;
