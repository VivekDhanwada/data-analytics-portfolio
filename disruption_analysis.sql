-- Q3: Alert frequency by type
SELECT alert_type, COUNT(alert_type) AS alert_count
FROM alerts_data
GROUP BY alert_type
ORDER BY alert_count DESC;

-- Q3: Alert frequency by type and month
SELECT alert_type, COUNT(alert_type) AS alert_count,
    EXTRACT(MONTH FROM start_time) AS alert_month
FROM alerts_data
GROUP BY alert_type, alert_month
ORDER BY alert_month, alert_count DESC;

-- Q3: Average alert duration by type and month
SELECT alert_type,
    EXTRACT(MONTH FROM start_time) AS alert_month,
    ROUND(EXTRACT(EPOCH FROM AVG(end_time - start_time))/3600, 2) AS avg_duration_hours
FROM alerts_data
GROUP BY alert_type, alert_month
ORDER BY avg_duration_hours DESC;