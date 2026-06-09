from typing import List
from app.agents.base import BaseAgent
from app.domain.entities.job import Job
from app.domain.interfaces.repositories import JobRepository
from app.scrapers.remotive_scraper import RemotiveScraper

class CollectorAgent(BaseAgent):
    """
    Agent responsible for collecting job offers from various sources.
    Analogy: The 'Harvester' that gathers raw materials (jobs) and stores them in the warehouse.
    """

    def __init__(self, job_repo: JobRepository):
        super().__init__(name="CollectorAgent")
        self.job_repo = job_repo
        self.scrapers = [
            RemotiveScraper()
            # Add other scrapers here as they are implemented
        ]

    async def run(self, keywords: str, location: str = "France") -> int:
        """
        Runs all scrapers and persists new jobs.
        Returns the number of new jobs collected.
        """
        self.log_start("collect_jobs", keywords=keywords, location=location)
        
        new_jobs_count = 0
        
        for scraper in self.scrapers:
            self.logger.info(f"Starting scraping from {scraper.source_name}")
            try:
                # Note: scrapers are currently sync, we wrap them or keep them sync if called from worker
                scraped_jobs = scraper.scrape(keywords=keywords, location=location)
                
                for sj in scraped_jobs:
                    # Duplicate detection by URL
                    existing = await self.job_repo.get_by_url(sj.url)
                    if existing:
                        continue
                        
                    # Create domain entity
                    job = Job(
                        title=sj.title,
                        description=sj.description,
                        company_name=sj.company,
                        location=sj.location,
                        job_type=sj.contract_type,
                        raw_url=sj.url
                    )
                    
                    await self.job_repo.save(job)
                    new_jobs_count += 1
                    
            except Exception as e:
                self.log_error(f"Scraping failed for {scraper.source_name}", e)

        self.log_end("collect_jobs", new_jobs_found=new_jobs_count)
        return new_jobs_count
