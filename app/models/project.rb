class Project < ApplicationRecord
  has_one_attached :file

  enum status: {
    pending: 0,
    processing: 1,
    failed: 2,
    completed: 3
  }

  broadcasts
end
