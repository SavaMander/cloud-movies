import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { MoviesService } from './movies.service';

describe('MoviesService', () => {
  let service: MoviesService;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [MoviesService]
    });
    service = TestBed.inject(MoviesService);
    httpTestingController = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpTestingController.verify();
  });

  it('should upload file to S3', () => {
    const file = new File(['sample content'], 'sample.txt', { type: 'text/plain' });
    const presignedURL = 'mock-presigned-url';

    service.uploadFileToS3(file, presignedURL).subscribe(response => {
      expect(response).toBeTruthy(); // Assert that the response is truthy
      // Add additional assertions if needed
    });

    const req = httpTestingController.expectOne(presignedURL);
    expect(req.request.method).toEqual('PUT'); // Assert that a PUT request is made
    expect(req.request.body).toEqual(file); // Assert that the file is sent in the request body

    // Respond to the request with a mock response
    req.flush({ /* mock response data */ });
  });

});
