$(document).ready(function(){
	var count = 1;
	var ratings = {};
	var round = 0;

	rating_event = function(){
		var joke_key = parseInt($(this).parent().parent().attr('joke'));
		var joke_rate = parseInt($(this).attr('class')[1]);
		
		ratings[joke_key] = joke_rate;
		console.log(ratings);
		
		if(count < jokes_count){
			$('.jokes').css('left', -900*count);
			$('#progress .bar').width(100*count/jokes_count+'%');
			$('#progress h3').html(count + ' / ' + jokes_count);
			count = count + 1;
		}else if(count == jokes_count){
			console.log("end");
			$('#progress .bar').width(100*count/jokes_count+'%');
			if(round == 0){
				$('#progress h3').html('Loading recommendations...');
			}else{
				$('#progress h3').html('Recalculating recommendations...');
			}
			if(round >0 && jokes_count < 10){
				alert("Dude, you have finished all the jokes. Go back to your work now!!");
				$('.round h2').html('Thanks for using Joke Butler Recommender System.');
				$('.jokes li').remove();
			}else{
				setTimeout(function(){
					$.ajax({
						type:'POST',
						url:'/',
						data: {ratings:JSON.stringify(ratings)}
					}).done(function(data){
						rec_data = JSON.parse(data);
						rec_jokes = rec_data['rec_jokes'];
						round = round + 1;
					
						$('.round h2').html('Round ' + round + ': Top 10 jokes recommended');
						$('.jokes li').remove();
						$('.jokes').css('left', 0);
						$('#progress .bar').width(0);
						jokes_count = rec_jokes.length;
						$('#progress h3').html('0 / ' + jokes_count);
						count = 1;
						for(var i=0; i<jokes_count; i++){
							var newline = '<li joke='+rec_jokes[i][0]+'>'+rec_jokes[i][1]+'<ul class="rates"><li class="r1"></li><li class="r2"></li><li class="r3"></li><li class="r4"></li><li class="r5"></li></ul></li>';
							$('.jokes').append(newline);
						}
						$('.rates li').on('click', rating_event);
					})
				}, 1000)
			}

		}
	}
	
	$('.rates li').on('click', rating_event);
});