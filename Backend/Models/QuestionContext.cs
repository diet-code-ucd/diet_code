using Microsoft.EntityFrameworkCore;

namespace Backend.Models;

public class QuestionContext : DbContext
{
    public QuestionContext(DbContextOptions<QuestionContext> options)
        : base(options)
    {
    }

    public DbSet<Question> Questions { get; set; } = null!;
}