import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def main():
	st.title('Recommendation System')
	st.markdown("Given a firm's portfolio, we want to recommend new firms as prospective clients.")
	st.image('undraw_business_deal_cpi9.png', use_column_width=True)

	clusters = pd.read_csv('clusters.csv', index_col=0)

	st.sidebar.title('Upload your portfolio:')
	file = st.sidebar.file_uploader('Select the *.csv file', type='csv')

	if file is None:
		st.sidebar.text("No file selected")

	if file is not None:
		portfolio = pd.read_csv(file, index_col=0)
		st.sidebar.markdown("Your portfolio has "+str(portfolio.shape[0])+" clients and "+
			str(portfolio.shape[1])+" columns.")

		n = st.sidebar.slider('Select the number of rows to visualize:', 1, 10)


		st.dataframe(portfolio.head(n))

		button = st.sidebar.button('Continue')

		if button:
				portfolio = pd.DataFrame(portfolio.loc[:, 'id'])
				portfolio['firms'] = 1

				join_data = pd.merge(clusters, portfolio, how='outer', on='id')
				join_data = join_data.fillna(0)

				cluster = join_data[join_data['firms'] == 1]
				rec = pd.DataFrame(cluster['clusters'].value_counts())
				rec.reset_index(inplace=True)
				cluster = rec.iloc[0, 0]

				cut0 = join_data[join_data['firms'] == 0]
				cut1 = cut0[cut0['clusters'] == cluster]
				firms_rec = cut1.loc[:, 'id']

				st.subheader("10 of the recommended clients:")
				st.markdown(list(firms_rec[0:11]))

if __name__ == '__main__':
	main()