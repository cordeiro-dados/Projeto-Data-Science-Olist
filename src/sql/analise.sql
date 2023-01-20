SELECT 
    T2.seller_id,
    SUM(T2.price) AS RECEITA_TOTAL,
    COUNT(DISTINCT T1.order_id) AS QTD_PEDIDOS,
    COUNT( T2.product_id) AS QTD_PRODUTOS,
    COUNT(DISTINCT T2.product_id) AS QTD_DISTINTA,
    MIN( DATE('2018-06-01') - T1.order_approved_at) AS QTD_DIAS_ULT_VENDA
FROM tb_orders AS T1

LEFT JOIN tb_order_items AS T2 
ON T1.order_id = T2.order_id

WHERE T1.order_approved_at BETWEEN '2017-06-01' AND '2018-06-01'

GROUP BY T2.seller_id