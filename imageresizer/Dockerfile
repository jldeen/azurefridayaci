FROM node:alpine

# Need for privileged ports
RUN apk add --no-cache libcap

# Create app directory
WORKDIR app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
# where available (npm@5+)
COPY package*.json ./

RUN npm install
# If you are building your code for production
# RUN npm install --only=production

# Bundle app source
COPY . .

# Set the privileges for our built app executable to run on privileged ports
RUN setcap 'cap_net_bind_service=+ep' /usr/local/bin/node

# Create user for App and give permissions to /app and /tmp folders
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && chown -R appuser /app /images
USER appuser

EXPOSE 80
CMD [ "npm", "start" ]
