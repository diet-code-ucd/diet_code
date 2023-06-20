using Backend.Models;
using Backend.Utils;


namespace Backend.Services;
public class TestService
{
    public Test GenerateTest(Course course, User user, int numberOfQuestions)
    {
        List<Question> availableQuestions = GetAvailableQuestions(course, user);
        availableQuestions.ShuffleList();
        List<Question> selectedQuestions = availableQuestions.Take(numberOfQuestions).ToList();
        if (selectedQuestions.Count < numberOfQuestions)
        {
            throw new Exception("Not enough questions available"); // Replace with OpenAI API call
        }
        Test test = new Test();
        test.Questions = selectedQuestions;
        return test;
    }
    private List<Question> GetAvailableQuestions(Course course, User user)
    {
        List<Question> previousQuestions = user.Tests.SelectMany(t => t.Questions).ToList();
        List<Question> availableQuestions = course.Questions.Except(previousQuestions).ToList() ?? new List<Question>();
        return availableQuestions;
    }
}