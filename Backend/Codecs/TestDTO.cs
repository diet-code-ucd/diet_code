namespace Backend.Models;

public class TestDTO {
    public int Id { get; set;}
    public virtual ICollection<int> Questions { get; set;}
    public virtual ICollection<int> Answers { get; set;}

    public static TestDTO FromTest(Test test) {
        return new TestDTO {
            Id = test.Id,
            Questions = test.Questions.Select(q => q.Id).ToList(),
            Answers = test.Answers.Select(a => a.Id).ToList()
        };
    }
}