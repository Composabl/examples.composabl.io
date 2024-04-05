# Composabl Simulators

This project contains all the simulators under `simulators/`

## Get Started
* Be sure that your docker app is installed and started

Open your terminal and go to the simulator folder:
```
cd simulators/public/cstr
```


Build the Docker image through the Dockerfile:
```
docker build -t composabl/sim-cstr .
```

Run the Docker image with your sim:
```
docker run -v /var/run/docker.sock:/var/run/docker.sock -it -p 1337:1337 composabl/sim-cstr
```

## Environment Variables

- `IS_HISTORIAN_ENABLED` : If set to `true`, the historian will be enabled. Defaults to `false`.
- `IS_REFLECTION_ENABLED`: If set to `true`, the reflection will be enabled. Defaults to `false`.

## Development

### Historian

We utilize dapr to be able to sink to the historian. As this should work across local, docker and kubernetes we use a mix of dapr standalone and not

