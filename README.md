# Prototipo de un Blog

Prototipo de un blog, diseñado para el levantamiento de la página web y la base de datos.

## Requisitos

1. Tener Docker instalados en tu máquina.
2. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables de entorno:

```
MYSQL_ROOT_PASSWORD=<contraseña_root>  
MYSQL_DATABASE=<nombre_base_datos>  
MYSQL_USER=<usuario_mysql>  
MYSQL_PASSWORD=<contraseña_mysql>  
SECRET_KEY=<clave_secreta>  
```

## Iniciar el Proyecto

Para levantar la página web y la base de datos, ejecuta el siguiente comando en la raíz del proyecto:

```docker-compose --env-file .env up -d```

Este comando inicializa los servicios definidos en el archivo `docker-compose.yml` y los ejecuta en segundo plano.

El proyecto estará disponible en el puerto **8080**.

## Creación y Recuperación de Cuenta

Para la creación y recuperación de cuentas, se enviará un **token** a través de la consola del navegador. Dependiendo de la acción que desees realizar, utiliza las siguientes URLs:

- Para crear una cuenta:  
  ```http://ip:8080/create?token=...```

- Para recuperar una cuenta:  
  ```http://ip:8080/recovery?token=...```

Sustituye `ip` con la dirección IP del servidor y `token` con el valor correspondiente.
