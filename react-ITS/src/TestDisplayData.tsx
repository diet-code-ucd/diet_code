import React, { useState, useEffect } from "react";

interface Question {
  question: string;
  answer: number;
  difficulty: string;
}

function Display() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [selectedQuestion, setSelectedQuestion] = useState<Question | null>(
    null
  );
  const [userAnswer, setUserAnswer] = useState("");
  const [isAnswerCorrect, setIsAnswerCorrect] = useState<boolean | null>(null);

  useEffect(() => {
    fetchQuestions();
  }, []);

  const fetchQuestions = () => {
    fetch("/TestQuestions.json")
      .then((response) => response.json())
      .then((data) => {
        setQuestions(data);
      })
      .catch((error) => {
        console.error("Error fetching questions:", error);
      });
  };

  const handleDifficultyChange = (
    event: React.ChangeEvent<HTMLSelectElement>
  ) => {
    const difficulty = event.target.value;
    const filteredQuestions = questions.filter(
      (question) => question.difficulty === difficulty
    );
    const randomIndex = Math.floor(Math.random() * filteredQuestions.length);
    setSelectedQuestion(filteredQuestions[randomIndex]);
    setUserAnswer("");
    setIsAnswerCorrect(null);
  };

  const handleAnswerSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    if (
      selectedQuestion &&
      selectedQuestion.answer === parseInt(userAnswer, 10)
    ) {
      setIsAnswerCorrect(true);
    } else {
      setIsAnswerCorrect(false);
    }
  };

  return (
    <div>
      <h1>Question:</h1>
      {selectedQuestion && (
        <div>
          <p>{selectedQuestion.question}</p>
          <form onSubmit={handleAnswerSubmit}>
            <label htmlFor="answer">Your Answer:</label>
            <input
              type="text"
              id="answer"
              value={userAnswer}
              onChange={(event) => setUserAnswer(event.target.value)}
            />
            <button type="submit">Submit</button>
          </form>
          {isAnswerCorrect !== null && (
            <p>Your answer is {isAnswerCorrect ? "correct" : "incorrect"}.</p>
          )}
        </div>
      )}
      <h2>Select Difficulty:</h2>
      <select onChange={handleDifficultyChange}>
        <option value="">Select</option>
        <option value="Easy">Easy</option>
        <option value="Medium">Medium</option>
        <option value="Hard">Hard</option>
        {/* Add more difficulty options based on your data */}
      </select>
    </div>
  );
}

export default Display;
