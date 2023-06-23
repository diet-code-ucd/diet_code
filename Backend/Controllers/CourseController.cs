using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Backend.Models;
using Backend.Codecs;

namespace Backend.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CourseController : ControllerBase
    {
        private readonly DatabaseContext _context;

        public CourseController(DatabaseContext context)
        {
            _context = context;
        }

        // GET: api/Course
        [HttpGet]
        public async Task<ActionResult<IEnumerable<CourseDTO>>> GetCourse()
        {
            if (_context.Course == null)
            {
                return NotFound();
            }
            var courses = await _context.Course.ToListAsync();
            return courses.Select(c => CourseDTO.FromCourse(c)).ToList();
        }

        // GET: api/Course/5
        [HttpGet("{id}")]
        public async Task<ActionResult<CourseDTO>> GetCourse(int id)
        {
            if (_context.Course == null)
            {
                return NotFound();
            }
            var course = await _context.Course.FindAsync(id);

            if (course == null)
            {
                return NotFound();
            }

            return CourseDTO.FromCourse(course);
        }

        // PUT: api/Course/5
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPut("{id}")]
        public async Task<IActionResult> PutCourse(int id, CourseDTO course)
        {
            if (id != course.Id)
            {
                return BadRequest();
            }

            var courseEntity = await _context.Course.FindAsync(id);
            if (courseEntity == null)
            {
                return NotFound();
            }
            courseEntity.Name = course.Name;
            courseEntity.Questions = course.Questions?.Select(q => _context.Question.Find(q)).ToList();
            _context.Entry(courseEntity).State = EntityState.Modified;

            try
            {
                await _context.SaveChangesAsync();
            }
            catch (DbUpdateConcurrencyException)
            {
                if (!CourseExists(id))
                {
                    return NotFound();
                }
                else
                {
                    throw;
                }
            }

            return NoContent();
        }

        // POST: api/Course
        // To protect from overposting attacks, see https://go.microsoft.com/fwlink/?linkid=2123754
        [HttpPost]
        public async Task<ActionResult<Course>> PostCourse(CourseDTO course)
        {
            if (_context.Course == null)
            {
                return Problem("Entity set 'DatabaseContext.Course'  is null.");
            }
            var courseEntity = new Course
            {
                Name = course.Name,
                Questions = course.Questions?.Select(q => _context.Question.Find(q)).ToList()
            };

            _context.Course.Add(courseEntity);

            await _context.SaveChangesAsync();

            return CreatedAtAction("GetCourse", new { id = course.Id }, course);
        }

        // DELETE: api/Course/5
        [HttpDelete("{id}")]
        public async Task<IActionResult> DeleteCourse(int id)
        {
            if (_context.Course == null)
            {
                return NotFound();
            }
            var course = await _context.Course.FindAsync(id);
            if (course == null)
            {
                return NotFound();
            }

            _context.Course.Remove(course);
            await _context.SaveChangesAsync();

            return NoContent();
        }

        private bool CourseExists(int id)
        {
            return (_context.Course?.Any(e => e.Id == id)).GetValueOrDefault();
        }
    }
}
