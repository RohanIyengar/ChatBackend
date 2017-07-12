# challenge-eng-base

To get the project up and running:
1. Install Docker https://docs.docker.com/engine/installation/
2. In a terminal, go to the directory `challenge-eng-base-master`
3. For a backend project
    1. `docker-compose up <project name>` (project name should be `backend-*` depending on your language of choice)
    2. Test that it's running http://localhost:18000/test
4. For a fullstack project
    1. Edit `docker-compose.yml`. Under `frontend-react`, change the `links` section to the backend project of your choice
    2. `docker-compose up frontend-react` (this will also spin up the linked backend project)
    3. Test that it's running http://localhost:13000/test

To stop and start a project
1. `docker-compose down`
2. `docker-compose up <project name>`

After making changes, you'll need to restart in order to see those changes reflected.

If you run into issues with connecting to the db on the first run, try restarting.
