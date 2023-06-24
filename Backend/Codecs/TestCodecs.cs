using Backend.Models;

namespace Backend.Codecs;

public class TestDTO {
    public int TestId { get; set;}
    public ICollection<QuestionDTO>? Questions { get; set;}

    public static TestDTO FromTest(Test test) {
        return new TestDTO {
            TestId = test.Id,
            Questions = test.Questions?.Select(q => new QuestionDTO {
                QuestionId = q.Id,
                Question = q.QuestionText
            }).ToList()
        };
    }
}

public class QuestionDTO {
    public int QuestionId { get; set;}
    public string Question { get; set;}
}

public class TestSubmission {
    public int TestId { get; set;}
    public virtual ICollection<QuestionSubmission>? Questions { get; set;}
}

public class QuestionSubmission {
    public int QuestionId { get; set;}
    public string Answer { get; set; }
}

public class TestResult {
    public int TestId { get; set;}
    public int NoOfQuestions { get; set;}
    public int NoOfCorrectAnswers { get; set;}
    public ICollection<QuestionResult>? Results { get; set;}
}

public class QuestionResult
{
    public string Question { get; set; }
    public string Answer { get; set; }
    public bool Correct { get; set; }
    public string CorrectAnswer { get; set; }
    public string Explanation { get; set; }

}