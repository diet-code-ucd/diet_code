namespace Backend.Models;

public class Question
{
    public int Id { get; set; }
    public string Query { get; set; }
    public ICollection<AnswerOption> Options { get; set; }
}