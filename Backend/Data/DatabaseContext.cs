using Backend.Data;
using Microsoft.EntityFrameworkCore;
using Backend.Models;

namespace Backend.Models;

public class DatabaseContext : DbContext
{
    public DatabaseContext(DbContextOptions<DatabaseContext> options)
        : base(options)
    {
        DbInitialiser.Initialise(this);

    }
    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseLazyLoadingProxies();
    }

    public DbSet<Backend.Models.User> Users { get; set; } = default!;

    public DbSet<Backend.Models.Course> Courses { get; set; } = default!;

    public DbSet<Backend.Models.Question> Questions { get; set; } = default!;

    public DbSet<Backend.Models.Test> Tests { get; set; } = default!;
}