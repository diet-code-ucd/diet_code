using Backend.Models;
using Microsoft.SemanticKernel;
using System.Text.Json;

namespace Backend.Services;

public interface IMLService
{
    public Task<List<Question>> GenerateQuestions(Course course, User user, Difficulty difficulty, int numberOfQuestions);
}

public class MLService : IMLService
{
    private readonly IKernel _kernel;

    public MLService()
    {
        var token = Environment.GetEnvironmentVariable("OPENAI_TOKEN");

        var builder = new KernelBuilder();
        builder.WithOpenAITextCompletionService(
            "text-davinci-003",
            token
            );

        _kernel = builder.Build();
    }

    public async Task<List<Question>> GenerateQuestions(Course course, User user, Difficulty difficulty, int numberOfQuestions)
    {
        string skPrompt = @"
You are a tutor helping a student with learning a subject.
You create questions along with answers and explanations.
The explanations are used to help the student understand the answer.

The difficulty of the questions are based as:
EASY = 0
MEDIUM = 1
HARD = 2

Responses are in JSON format.

Here is a sample JSON response with 3 questions:
--- BEGIN SAMPLE RESPONSE ---
[
  {
    ""QuestionText"": ""What is the value of pi?"",
    ""Answer"": ""3.14"",
    ""Difficulty"": 0,
    ""Explanation"": ""Pi is a mathematical constant that represents the ratio of a circle's circumference to its diameter.""
  },
  {
    ""QuestionText"": ""What is the square root of 64?"",
    ""Answer"": ""8"",
    ""Difficulty"": 0,
    ""Explanation"": ""The square root of a number is the value that, when multiplied by itself, gives the original number.""
  },
  {
    ""QuestionText"": ""What is the sum of 5 and 7?"",
    ""Answer"": ""12"",
    ""Difficulty"": 0,
    ""Explanation"": ""The sum of two numbers is the result of adding them together.""
  }
]
--- END SAMPLE RESPONSE ---

{{$input}}

" + $"Create {numberOfQuestions} questions.";

        var age = user.DateOfBirth.Year - DateTime.Now.Year;

        var textToSummarize = $"""
        The student is learning {course.Name}.
        The student is {age} years old.
        The answers should be appropriate for a the student's age.
        The difficulty of the questions should be {difficulty} difficulty.
        """;

        var tldrFunction = _kernel.CreateSemanticFunction(skPrompt, maxTokens: 2000, temperature: 0, topP: 0.5);

        var summary = await tldrFunction.InvokeAsync(textToSummarize);
        
        var summaryText = summary.ToString();
        var startIndex = summaryText.IndexOf("[");
        var endIndex = summaryText.LastIndexOf("]");
        summaryText = summaryText.Substring(startIndex, endIndex - startIndex + 1);

        Console.WriteLine(summary); 

        List<Question> questions = JsonSerializer.Deserialize<List<Question>>(summaryText);
        
        return questions; 
    }
}
