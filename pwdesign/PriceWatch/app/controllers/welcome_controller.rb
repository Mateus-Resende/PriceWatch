class WelcomeController < ApplicationController
  def index
  	@products = Product.paginate(:per_page => 5, :page => params[:page])
  end
end
