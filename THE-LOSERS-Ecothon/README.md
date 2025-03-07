# THE LOSERS Ecothon Project

## Overview
The "THE LOSERS Ecothon" project is an energy management system designed to monitor and control energy consumption across various facilities. The application features an admin dashboard for data visualization and a login page for user authentication.

## Project Structure
```
THE-LOSERS-Ecothon
├── src
│   ├── index.html        # Main dashboard page
│   ├── login.html        # Login page with Google OAuth2
│   ├── app.js            # Client-side logic for authentication and session management
│   └── styles
│       └── main.css      # CSS styles for the application
├── package.json          # npm configuration file
├── README.md             # Project documentation
└── server.js             # Server-side logic and routing
```

## Setup Instructions

1. **Clone the Repository**
   ```
   git clone <repository-url>
   cd THE-LOSERS-Ecothon
   ```

2. **Install Dependencies**
   Ensure you have Node.js installed. Then run:
   ```
   npm install
   ```

3. **Configure Google OAuth2**
   - Create a project in the Google Developer Console.
   - Enable the Google OAuth2 API.
   - Create OAuth 2.0 credentials and set the redirect URI to your server's callback endpoint.
   - Store your client ID and client secret in a secure location.

4. **Run the Server**
   Start the server using:
   ```
   node server.js
   ```

5. **Access the Application**
   Open your browser and navigate to `http://localhost:3000` to access the login page.

## Usage Guidelines
- Users can log in using the "Login with Google" button, which redirects to the Google OAuth2 login page.
- Upon successful authentication, user details will be retrieved and stored in the session.
- Access to the admin dashboard is restricted to authenticated users only.
- Users can log out, which will clear the session data.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License.