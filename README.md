# TikTok Video Generator

This project uses Docker to run a Python application that generates TikTok videos. The application takes several command-line arguments to customize its operation.

## Prerequisites

You need Docker installed on your machine. Follow the installation guide for your platform [here](https://docs.docker.com/get-docker/).

You need Chrome installed on you machine.

## Project Setup

**Copy config and fill it:**
`cp app/config.yaml.example app/config.yaml`


## Docker Setup and Usage

1. **Build the Docker image:**

Navigate to the directory containing the `Dockerfile` and `docker-compose.yml` files, then run:

```shell
docker-compose build
```

2. **Run the Python application in a Docker container:**

You can customize the operation of the Python application using command-line arguments. Here is an example command that runs the application with the 'reddit' function and French as the destination language:

```shell
docker-compose run your-python-app python ./app/__main__.py -f reddit -l fr-FR
```


## Command-Line Arguments

- `-f`, `--func`: Function to use (default: 'reddit')
- `-l`, `--lang`: Destination language (default: 'fr-FR')
- `-fl`, `--fromlang`: Original language (default: 'en-EN')
- `--subreddit`: If used with the 'reddit' function, specifies the subreddit (default: 'AskReddit')
- `--lp`: If used with the 'reddit' function, sets the post limit (default: 5)
- `--lc`: If used with the 'reddit' function, sets the comment limit (default: 5)
- `--file`: Specifies the output file directory (default: 'app/output/')
- `--elevenlabs`: Boolean flag (default: False)
- `--option`: Specifies an optional parameter (default: None)
- `--facts`: Specifies the number of facts to generate (default: 7)

For example, to run the application with the 'reddit' function, English as the original language, and 'AskReddit' as the subreddit, you would use:

```shell
docker-compose run your-python-app python ./app/__main__.py -f reddit -fl en-EN --subreddit AskReddit
```

Please refer to the Python script documentation or use the `-h` flag for further details on the command-line arguments:

```shell
docker-compose run your-python-app python ./app/__main__.py -h
```

## Usage

1. **Basic usage :**
```shell
docker-compose run tiktok-maker python app/__main__.py -f {function} -l {lang to translate to}
```

### Usage Examples
```shell
docker-compose run tiktok-maker python app/__main__.py -f randomgen -l fr-FR  --elevenlabs True 
```
```shell
docker-compose run tiktok-maker python app/__main__.py -f reddit -l fr-FR --subreddit AskReddit --lp 5 --lc 8 --elevenlabs True
```

## Recovering files
```shell

```

## Note

The Docker container does not persist data. Files created during the execution of the Python application will be lost once the container is stopped. If you need to persist data, consider mounting a Docker volume.
