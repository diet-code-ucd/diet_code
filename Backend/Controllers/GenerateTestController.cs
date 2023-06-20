using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Backend.Models;
using Backend.Codecs;

using Backend.Services;

namespace Backend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class GenerateTestController : ControllerBase
    {
        private readonly DatabaseContext _context;

        public GenerateTestController(DatabaseContext context)
        {
            _context = context;
        }

        // POST: api/User
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<Test>> PostGenerateTest(GenerateTest generateTest)
        {
            var course = await _context.Course.FindAsync(generateTest.CourseId);
            var user = await _context.Users.FindAsync(generateTest.UserId);
            if (course == null || user == null)
            {
                return NotFound();
            }
            Test test = TestService.GenerateTest(course, user, generateTest.NumberOfQuestions, _context);

            _context.Test.Add(test);
            await _context.SaveChangesAsync();

            user.Tests.Add(test);

            _context.Entry(user).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                throw;
            }

            return test;
        }
    }
}
