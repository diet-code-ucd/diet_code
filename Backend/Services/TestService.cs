using Backend.Codecs;
using Backend.Models;
using Backend.Utils;
using Microsoft.EntityFrameworkCore;

namespace Backend.Services;

public interface ITestService
{
    public Task<Test> GenerateTest(Course course, User user, Difficulty difficulty, int numberOfQuestions);
    public TestResult GradeTest(TestSubmission test);
}

public class TestService : ITestService
{
    private readonly DatabaseContext _context;
    private readonly IMLService _mlService;

    public TestService(DatabaseContext context, IMLService mlService)
    {
        _context = context;
        _mlService = mlService;
    }


    public async Task<Test> GenerateTest(Course course, User user, Difficulty difficulty, int numberOfQuestions)
    {
        List<Question> availableQuestions = GetAvailableQuestions(course, user, difficulty);
        availableQuestions.ShuffleList();
        List<Question> selectedQuestions = availableQuestions.Take(numberOfQuestions).ToList();
        if (selectedQuestions.Count < numberOfQuestions)
        {
          List<Question> newQuestions = await _mlService.GenerateQuestions(course, user, difficulty, numberOfQuestions - selectedQuestions.Count);
          // Add new questions to the course
          newQuestions.ForEach(q => course.Questions.Add(q));
          _context.AddRange(newQuestions);
          _context.Entry(course).State = EntityState.Modified;
          await _context.SaveChangesAsync();
          selectedQuestions.AddRange(newQuestions);
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
