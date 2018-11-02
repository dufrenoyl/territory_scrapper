ScriptR=function(csv, csv2, csv3){
	library(gridExtra)
	library(plotrix)	

	#We read the first 50rst rows of the first csv 
	a=read.csv(csv, nrow=50)

	#We split the name to keep the part before .csv
	plotfile = strsplit(csv,".csv")
	print(plotfile[[1]])

	#We create and open a pdf file
	pdf(file=paste(plotfile[[1]],".pdf",sep=""))

	# We create a vector color
	color=c("blue","red")
	
	#Plot about price difference
	c=rbind(a $DIFFPRICE)
	b=barplot(c,beside=F,xlab="OnD",ylab="Diff Price (1A - ITA en $)", col="green",cex.names=0.4)

	#We print the OnDs
	text(b,par("usr")[3],labels =paste(a$ORIGIN,a$DEST,sep=""),srt = 45, adj = c(1.1,1.1), xpd = TRUE, cex=.4)

	#We put a title for the plot
	title(main="Price difference", col.main="red", font.main=4)

	#Plot to compare 1A and ITA prices
	#Vector price (price1 = Amadeus' price, price2 = ITA's price)
	c=rbind(a $PRICE1, a $PRICE2)
	b=barplot(c,beside=T,xlab="OnD", ylab="Price (en $)", col=c("darkblue","red"),legend=c("AMADEUS","ITA"),cex.names=0.4)
)
	#We print the OnDs
	text(b,par("usr")[3],labels =paste(a$ORIGIN,a$DEST,sep=""),srt = 45, adj = c(1.1,1.1), xpd = TRUE, cex=.4)
	
	#Title for the plot
	title(main="Price proposed by 1A and ITA", col.main="red", font.main=4)

	# we read the csv file
	aa = read.csv(csv)	
	
	#We get back information from the column DIFFPRICE
	summa = summary(aa $DIFFPRICE)

	#nb DIFFPRICE < 0
	sum1A = sum(aa $DIFFPRICE < 0)
	#nb DIFFPRICE > 0
	sumITA = sum(aa $DIFFPRICE > 0)
	sumEg = sum(aa $DIFFPRICE == 0)
	print(summa)
	print(sum1A)
	print(sumITA)
	print(sumEg)

	#We print them in a plot then we put it in the pdf file
	plot(0:10, type="n", xaxt="n", yaxt="n", bty="n", xlab="", ylab="")
	text(5,10,paste("Min difference: ", summa[[1]],sep=" "))
	text(5,9,paste("Max difference:", summa[[6]],sep=" "))
	text(5,8,paste("1A cheaper than ITA: ", sum1A,sep=" "))
	text(5,7,paste("ITA cheaper than 1A: ", sumITA,sep=" "))
	text(5,6,paste("1A same as ITA: ", sumEg,sep=" "))
	

	#Pie chart to exploit results that we found before
	slices = c(sum1A, sumITA, sumEg)
	lbls = c("AMADEUS","ITA","EQUAL")
	pct = round(slices/sum(slices)*100)
	lbls = paste(lbls,pct)
	lbls = paste(lbls,"%",sep="")
	pie(slices,labels=lbls, col=rainbow(length(lbls)),main="Pie chart, Cheapest Price repartition")

	## FOR AMADEUS ##
	#We read the third csv
	aaa = read.csv(csv3)
	diff = aaa $NB1A-aaa $TOTALBC1A
	#Pie chart to show the bad click repartition
	#vector badclick , good click
	slices3 = c(aaa $TOTALBC1A, diff)
	lbls3 = c("Bad click","No Bad click")
	pct3 = round(slices3/sum(slices3)*100)
	lbls3 = paste(lbls3,pct3)
	lbls3 = paste(lbls3,"%",sep="")
	pie(slices3,labels=lbls3, col=rainbow(length(lbls3)),main="Pie chart, Bad click for AMADEUS")

	## FOR ITA ##
	#Pie chart to show the bad click repartition
	#vector badclick , good click
	diff2 = aaa $NBITA-aaa $TOTALBCITA
	slices2 = c(aaa $TOTALBCITA, diff2)
	lbls2 = c("Bad click","Good click")
	pct2 = round(slices2/sum(slices2)*100)
	lbls2 = paste(lbls2,pct2)
	lbls2 = paste(lbls2,"%",sep="")
	pie(slices2,labels=lbls2, col=rainbow(length(lbls2)),main="Pie chart, Bad click for ITA")

	#Summary of cheapness system on each OnD
	grid.newpage()
	df = read.csv(csv2)
	eqOnD = as.data.frame(df[1,])

	for (i in 2:nrow(df))
	{
		eqOnD = rbind(eqOnD, df[i,])
	}
	
	grid.table(eqOnD,show.rownames=FALSE,gpar.coretext=gpar(fontsize=8, col="slateblue"),gpar.coltext=gpar(col="black",cex=0.7))
	
	# We close the pdf file
	dev.off()

	return(a)
}
