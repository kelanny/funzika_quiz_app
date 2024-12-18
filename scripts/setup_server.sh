#!/usr/bin/bash
# Prepares and configure Server environment

# Function to install MySQL (Database Server)
install_mysql() {
  if ! command -v mysql &> /dev/null; then
    echo "MySQL not found. Installing MySQL..."

    # Update apt repository
    sudo apt-get update

    # Install mysql
    sudo apt-get install mysql-server

    # Start mysql service
    sudo service mysql start

    # Allow to start with system initialization
    sudo service mysql restart

    # Check Server status
    sudo service mysql status

    echo "MySQL installation completed and service started."

  else
    echo "MySQL is already installed."
  fi
}

# Function to install Nginx
install_nginx() {
  if ! command -v nginx &> /dev/null; then
    echo "Nginx not found. Installing Nginx..."
    sudo apt-get install -y nginx
    sudo systemctl start nginx
    sudo systemctl enable nginx
    echo "Nginx installation completed and service started."
  else
    echo "Nginx is already installed."
  fi
}
# Function to install gunicorn (Application Server)
install_gunicorn() {
        pip3 install gunicorn
        echo "Application server installation completed succesfully."
}

# Main function
main() {
        install_mysql
        install_nginx
        install_gunicorn
}

main
echo "App setup completed successfully"
