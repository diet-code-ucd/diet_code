import React, { useEffect, useState } from "react";
import axios from "axios";
import CourseSelection from "./CourseSelection";

interface TestQuestion {
  questionId: number;
  question: string;
  answer: string;
}

interface TestResult {
  question: string;
  answer: string;
  correct: boolean;
  correctAnswer: string;
  explanation: string;
}

interface TestPageProps {
  userId: number;
  courseId: number;
  numberOfQuestions: number;
  difficulty: number;
}

const TestPage: React.FC<TestPageProps> = ({
  userId = 1,
  courseId = 1,
  numberOfQuestions = 5,
  difficulty = 0,
}) => {
  const [testId, setTestId] = useState<number>(0);
  const [questions, setQuestions] = useState<TestQuestion[]>([]);
  const [submitted, setSubmitted] = useState<boolean>(false);
  const [results, setResults] = useState<TestResult[]>([]);

  // Function to generate the test
  const generateTest = async () => {
    try {
      const requestBody = {
        userId,
        courseId,
        numberOfQuestions,
        difficulty,
      };

      const response = await axios.post(
        "http://localhost:5057/api/Test/generate",
        requestBody
      );
      console.log(response);
      const { testId, questions } = response.data;
      setTestId(testId);
      setQuestions(
        questions.map((question: any) => ({
          questionId: question.questionId,
          question: question.question,
          answer: "",
        }))
      );
    } catch (error) {
      console.error("Error generating test:", error);
    }
  };

  // Function to handle answer input change
  const handleAnswerChange = (
    event: React.ChangeEvent<HTMLInputElement>,
    questionId: number
  ) => {
    const answer = event.target.value;

    setQuestions((prevQuestions) =>
      prevQuestions.map((question) =>
        question.questionId === questionId ? { ...question, answer } : question
      )
    );
  };

  // Function to handle form submission
  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    try {
      // Prepare the answers data
      const answers = questions.map((question) => ({
        questionId: question.questionId,
        answer: question.answer,
      }));

      // Make the API request to submit the answers
      const response = await axios.post(
        `http://localhost:5057/api/Test/submit`,
        {
          testId,
          questions: answers,
        }
      );

      // Handle the response
      const { results } = response.data;
      setResults(results);
      setSubmitted(true);
    } catch (error) {
      console.error("Error submitting answers:", error);
    }
  };

  return (
    <div>
      <h2>Test Page</h2>
      {!submitted ? (
        <button onClick={generateTest}>Generate Test</button>
      ) : (
        <div>
          <h3>Test Results</h3>
          <p>Total Questions: {results.length}</p>
          <p>
            Correct Answers: {results.filter((result) => result.correct).length}
          </p>
          <p>
            Incorrect Answers:{" "}
            {results.filter((result) => !result.correct).length}
          </p>
          {results.map((result) => (
            <div key={result.question}>
              <p>Question: {result.question}</p>
              <p>Your Answer: {result.answer}</p>
              {!result.correct && (
                <>
                  <p>Correct Answer: {result.correctAnswer}</p>
                  <p>Explanation: {result.explanation}</p>
                </>
              )}
              <hr />
            </div>
          ))}
        </div>
      )}
      {!submitted && (
        <form onSubmit={handleSubmit}>
          {questions.map((question) => (
            <div key={question.questionId}>
              <p>{question.question}</p>
              <input
                type="text"
                value={question.answer}
                onChange={(event) =>
                  handleAnswerChange(event, question.questionId)
                }
              />
            </div>
          ))}
          <button type="submit">Submit</button>
        </form>
      )}
    </div>
  );
};

export default TestPage;
