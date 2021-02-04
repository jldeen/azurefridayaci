FROM node:alpine

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

# Create user for App and give permissions to /app and /tmp folders
RUN addgroup -S appgroup && adduser -S appuser -G appgroup && chown -R appuser /app /tmp
USER appuser

EXPOSE 80
CMD [ "npm", "start" ]
