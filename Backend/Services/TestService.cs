using Backend.Codecs;
using Backend.Models;
using Backend.Utils;


namespace Backend.Services;

public interface ITestService
{
    public Test GenerateTest(Course course, User user, Difficulty difficulty, int numberOfQuestions);
    public TestResult GradeTest(TestSubmission test);
}
public class TestService : ITestService
{
    private readonly DatabaseContext _context;
    public TestService(DatabaseContext context)
    {
        _context = context;
    }
    public Test GenerateTest(Course course, User user, Difficulty difficulty, int numberOfQuestions)
    {
        List<Question> availableQuestions = GetAvailableQuestions(course, user, difficulty);
        availableQuestions.ShuffleList();
        List<Question> selectedQuestions = availableQuestions.Take(numberOfQuestions).ToList();
        if (selectedQuestions.Count < numberOfQuestions)
        {
            throw new Exception("Not enough questions available"); // Replace with OpenAI API call
        }
        Test test = new Test{
            Questions = selectedQuestions
        };
        return test;
    }

    public TestResult GradeTest(TestSubmission test)
    {
        TestResult result = new TestResult{
            TestId = test.TestId,
            NoOfQuestions = test.Questions.Count,
            NoOfCorrectAnswers = 0,
            Results = new List<QuestionResult>()
        };
        foreach (QuestionSubmission question in test.Questions)
        {
            Question q = _context.Questions.Find(question.QuestionId);
            QuestionResult questionResult = new QuestionResult{
                Question = q.QuestionText,
                Answer = question.Answer,
                Correct = q.Answer == question.Answer,
                CorrectAnswer = q.Answer,
                Explanation = q.Explanation
            };
            if (questionResult.Correct)
            {
                result.NoOfCorrectAnswers++;
            }
            result.Results.Add(questionResult);
        }
        return result;
    }

    private List<Question> GetAvailableQuestions(Course course, User user, Difficulty difficulty)
    {
        List<Question> previousQuestions = user.Tests.SelectMany(t => t.Questions).ToList() ?? new List<Question>();
        List<Question> availableQuestions = course.Questions.Where(q => q.Difficulty == difficulty).Except(previousQuestions).ToList() ?? new List<Question>();
        return availableQuestions;
    }
}