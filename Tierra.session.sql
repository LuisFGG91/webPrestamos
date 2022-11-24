select * from venta ;

select * from detalleventa ;

select * from articulo ;

select * from anticipo ;

select * from vendedor ;

select * from cliente ;

select * from grupo ;

select * from categoria ;

select * from infoventa_vendedor ;

select * from comisionvendedor ;

select * from comision_venta_vendedor;









/*

Existe el pago de una asignación especial que considera el número de ventas mensuales de cada vendedor. 



De esta forma si el vendedor posee 10 o más ventas en el mes se hace acreedor a una asignación que corresponde al 15% del monto neto de sus ventas; 

La asignación será de un 12% si posee entre 8 y 9 ventas, 

de un 10% si efectuó entre 6 y 7 ventas.

De un 8% si tiene entre 3 y 5 ventas y de un 5% si tiene entre 1 y 2 ventas. 

No aplica asignación si no tiene ventas. 



Los porcentajes aplicables a esta asignación varían mensualmente, por lo que deben ingresarse mediante variables BIND.

*/



/*

10 >= 15%

8 and 9 = 12%

6 and 7 = 10%

3 and 5 = 8%

1 and 2 = 5%

0 = 0%

*/





/*



Existe el pago mensual de una Asignación Especial por concepto de antigüedad, el que también se debe

calcular sobre el monto neto de las ventas. 



La regla de negocio establece que si el vendedor lleva vinculado a

la empresa más de 10 años le corresponde un bono equivalente a un 22% de su venta neta,

de un 16% si tiene entre 6 y 10 años de antigüedad, 

de un 7% si tiene entre 3 y 5 años de antigüedad. 



El bono no es aplicable en cualquier otro caso. 



*/

declare  



por_10 int := to_number('0123456789');

por_entre_8_and_9 int := to_number('0123456789');

por_entre_6_and_7 int := to_number('0123456789');

por_entre_3_and_5 int := to_number('0123456789');

por_entre_1_and_2 int := to_number('0123456789');

por_entre_0 int := to_number('0123456789');

begin 



select 

EXTRACT(YEAR FROM FECHA_VENTA) AS ANOO ,

EXTRACT(MONTH FROM FECHA_VENTA) AS MES ,

vn.id_vendedor,

VN.NOMBRES ||' '|| VN.APELLIDOS as NOMBRE, 

gr.nom_grupo,

count(VE.ID_VENTA) AS NRO_VENTAS ,

SUM(DV.CANTIDAD * AR.PRECIO) AS VENTAS_NETAS_MES ,

round((SUM(DV.CANTIDAD * AR.PRECIO)/100) * gr.porc,0) as Bono_Grupo,

round((SUM(DV.CANTIDAD * AR.PRECIO)/100) * ca.porcentaje,0) as Incentivo_Categoria,

ROUND(case 

when count(VE.ID_VENTA) >= 10 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 15 --por_10

when count(VE.ID_VENTA) BETWEEN 8 and 9 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 12--por_entre_8_and_9

when count(VE.ID_VENTA) BETWEEN 6 and 7 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 10--por_entre_6_and_7

when count(VE.ID_VENTA) BETWEEN 3 and 5 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 8 --por_entre_3_and_5

when count(VE.ID_VENTA) BETWEEN 1 AND 2 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 5 --por_entre_1_and_2

else

  SUM(DV.CANTIDAD * AR.PRECIO) * 0-- por_entre_0

end ,0)as ASIGNACION_VTAS ,

ROUND(case 

when trunc(months_between(sysdate,vn.feccontrato)/12) > 10 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 22 --por_10

when trunc(months_between(sysdate,vn.feccontrato)/12) BETWEEN 6 and 10 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 16--por_entre_8_and_9

when trunc(months_between(sysdate,vn.feccontrato)/12) BETWEEN 3 and 5 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 7--por_entre_6_and_7

else

  SUM(DV.CANTIDAD * AR.PRECIO) * 0-- por_entre_0

end ,0)as ASIGNACION_Antiguedad ,

NVL(sum(an.monto),0) as anticipos,





SUM(DV.CANTIDAD * AR.PRECIO) +



round((SUM(DV.CANTIDAD * AR.PRECIO)/100) * gr.porc,0) +

round((SUM(DV.CANTIDAD * AR.PRECIO)/100) * ca.porcentaje,0) +

ROUND(case 

when count(VE.ID_VENTA) >= 10 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 15 --por_10

when count(VE.ID_VENTA) BETWEEN 8 and 9 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 12--por_entre_8_and_9

when count(VE.ID_VENTA) BETWEEN 6 and 7 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 10--por_entre_6_and_7

when count(VE.ID_VENTA) BETWEEN 3 and 5 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 8 --por_entre_3_and_5

when count(VE.ID_VENTA) BETWEEN 1 AND 2 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 5 --por_entre_1_and_2

else

  SUM(DV.CANTIDAD * AR.PRECIO) * 0-- por_entre_0

end ,0) +

ROUND(case 

when trunc(months_between(sysdate,vn.feccontrato)/12) > 10 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 22 --por_10

when trunc(months_between(sysdate,vn.feccontrato)/12) BETWEEN 6 and 10 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 16--por_entre_8_and_9

when trunc(months_between(sysdate,vn.feccontrato)/12) BETWEEN 3 and 5 then (SUM(DV.CANTIDAD * AR.PRECIO)/100) * 7--por_entre_6_and_7

else

  SUM(DV.CANTIDAD * AR.PRECIO) * 0-- por_entre_0

end ,0) - 



NVL(sum(an.monto),0) as valor_total



from vendedor Vn

left join venta Ve on ve.id_vendedor = vn.id_vendedor 

left join detalleventa dv on dv.id_venta = ve.id_venta

left join articulo ar on ar.id_articulo = dv.id_articulo

left join categoria ca on ca.id_categoria = vn.id_categoria

left join grupo gr on gr.id_grupo = vn.id_grupo

left join anticipo an on an.id_vendedor = vn.id_vendedor and 

an.mes = EXTRACT(month FROM fecha_venta)

where EXTRACT(month FROM fecha_venta) = 5

group by vn.rut_vendedor , vn.nombres, vn.apellidos,vn.id_vendedor,gr.nom_grupo,gr.porc

,EXTRACT(year FROM fecha_venta) ,

EXTRACT(month FROM fecha_venta),ca.nom_categoria,ca.porcentaje,vn.feccontrato