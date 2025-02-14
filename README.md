# Funzika Quiz Application

A dynamic and user-friendly web application designed for creating, taking, and managing quizzes. This project allows users to test their knowledge in a variety of topics while providing administrators the tools to create and manage quizzes efficiently.

---

## 🚀 Features

- **User Authentication:** Secure sign-up and login functionality.
- **Quiz Management:** Admins can create, update, and delete quizzes and their questions.
- **Real-time Quiz Interface:** Users can attempt quizzes with interactive features such as instant feedback.
- **Result Analysis:** Users receive detailed results with scores and performance insights after completing a quiz.
- **Responsive Design:** Optimized for desktop and mobile devices.
- **Scalable Architecture:** Built with a modular and maintainable codebase.

---

## 🛠️ Technologies Used

- **Frontend:** HTML, CSS, Bootstrap, JavaScript (optional for interactivity)
- **Backend:** Python (Flask)
- **Database:** MySQL
- **Deployment:** Docker, Gunicorn, Nginx
- **Version Control:** Git

---

## 📂 Folder Structure

```
├── /app            # Application files including models and routes
│   ├── __init__.py # Initialize the app module
│   ├── /quiz # Handles database interactions
│   ├── /question     # Database models
│   ├── /answer     # Flask routes (APIs and views)
├── /static         # CSS, JavaScript, and images
├── /templates      # HTML templates for frontend views
├── /tests          # Unit and integration tests
├── config.py       # Application configuration
├── run.py          # Main application entry point
└── README.md       # Project documentation
```

---

## 🎯 Target Audience

- **Students & Educators:** To create and attempt educational quizzes for learning purposes.
- **Corporate Trainers:** To evaluate and analyze employee knowledge through interactive quizzes.
- **General Users:** Anyone who enjoys testing their knowledge with fun quizzes.

---

## 🔧 Installation

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/kelanny/funzika-quiz-app.git
   cd funzika-quiz-app
   ```

2. **Set Up Virtual Environment:**
   ```bash
   python3 -m venv funzika_env
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Database:**
   - Configure the database credentials in `config.py`.
   - Run database migrations to create the schema.

5. **Run the Application:**
   ```bash
   flask run
   ```

6. **Access the App:**
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## 🔗 Live Demo

_**(Add live deployment link here once the app is deployed)**_

---

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Create a pull request.

---

## 🧪 Testing

To run the unit and integration tests:
```bash
pytest
```
Ensure all tests pass before making a pull request.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

## 📧 Contact

For any inquiries or feedback, feel free to reach out:
- **Email:** mburukelvin@gmail.com
- **GitHub:** [@kelanny](https://github.com/kelanny)

---

Happy quizzing! 🎉
